from fastapi import FastAPI, Response


app = FastAPI()

@app.get("/data/xml", summary="返回XML格式数据")
def get_xml_data():
    xml_content = """
    <?xml version="1.0"?>
        <user>
           <id>1</id>
           <username>test_user</username>
           <email>test@example.com</email>
        </user>
"""
    # 直接通过Response返回自定义媒体类型的响应
    return Response(
        content=xml_content,
        media_type="application/xml",
        status_code=200
    )