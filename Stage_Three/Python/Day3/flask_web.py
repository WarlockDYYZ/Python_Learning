from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import time
from sqlalchemy import update


app = Flask(__name__)
# 配置SQLAlchemy连接池（针对高并发优化）
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:your_password@localhost/order_db'
app.config['SQLALCHEMY_POOL_SIZE'] = 50  # 连接池大小
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 50  # 溢出连接数
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 5  # 连接超时
app.config['SQLALCHEMY_POOL_RECYCLE'] = 300  # 连接回收时间, 针对 "空闲状态" 连接
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对数据库模型对象修改的自动追踪功能。
db = SQLAlchemy(app)


# 定义模型
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    stock = db.Column(db.Integer)  # 库存数量
    price = db.Column(db.Float)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    total_price = db.Column(db.Float)
    status = db.Column(db.String(20))  # 订单状态
    create_time = db.Column(db.DateTime)


@app.route('/order/submit', methods=['POST'])
def submit_order():
    """提交订单接口"""
    try:
        data = request.get_json()
        user_id = data['user_id']
        product_id = data['product_id']
        quantity = data['quantity']

        # 开启事务
        # db.session.begin_nested()

        # 1. 检查库存
        product = Product.query.get(product_id)
        if product.stock < quantity:
            raise ValueError("库存不足")

        # 2. 扣减库存
        # ORM 对象操作方式，有一定不足
        # product.stock -= quantity
        # db.session.add(product)  # 通过 get 获取的对象不需要提交

        # 使用数据库层面的原子操作扣减库存（乐观锁思想）
        # 在 UPDATE 时带上 `Product.stock >= quantity` 条件，确保绝对不会超卖
        affected_rows = db.session.execute(
            update(Product)
            .where(Product.id == product_id)
            .where(Product.stock >= quantity)
            .values(stock=Product.stock - quantity)
        ).rowcount

        # 如果受影响的行数为 0，说明在此期间有其他线程抢先扣减了库存
        if affected_rows == 0:
            raise ValueError("库存已被抢购一空，请重试")

        # 3. 创建订单
        order = Order(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity,
            total_price=product.price * quantity,
            status='已提交',
            create_time=time.strftime('%Y-%m-%d %H:%M:%S')
        )
        db.session.add(order)

        # 4. 提交事务
        db.session.commit()

        return jsonify({
            'code': 0,
            'message': '订单提交成功',
            'order_id': order.id
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'code': -1,
            'message': f'订单提交失败: {str(e)}'
        })


if __name__ == '__main__':
   app.run(threaded=True, port=5000)