from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
import uuid
from datetime import datetime
import random

from ..database import get_db
from ..models.models import DiseaseRecord
from ..models.schemas import DiseaseAnalyzeResponse, DiseaseHistoryResponse, MessageResponse
from ..config import settings

router = APIRouter(prefix="/disease", tags=["病虫害识别"])

# 病虫害数据库(模拟)
DISEASE_DATABASE = {
    "稻瘟病": {
        "symptoms": "叶片出现纺锤形褐色病斑，中央灰白色，边缘褐色。病斑多时汇合成不规则形，严重时叶片枯死。在潮湿条件下，病斑背面产生灰绿色霉层。",
        "advices": [
            "选用抗病品种，合理布局品种",
            "发病初期及时喷药防治，可选用三环唑、稻瘟灵等",
            "合理施肥，避免氮肥过量，增施磷钾肥",
            "田间发现中心病株时，应立即喷药封锁",
            "收获后及时清理病残体，减少菌源"
        ],
        "drugs": ["三环唑", "稻瘟灵", "富士一号", "春雷霉素"]
    },
    "纹枯病": {
        "symptoms": "主要为害叶鞘和叶片。初期在近水面的叶鞘上出现暗绿色水渍状小斑，逐渐扩大成椭圆形或云纹状病斑，边缘褐色，中央灰白色。",
        "advices": [
            "合理密植，改善田间通风透光条件",
            "科学施肥，避免氮肥过量",
            "发病初期喷施井冈霉素或噻呋酰胺",
            "及时清除田间杂草"
        ],
        "drugs": ["井冈霉素", "噻呋酰胺", "苯醚甲环唑"]
    },
    "蚜虫": {
        "symptoms": "成虫和若虫群集在叶片背面和嫩茎上吸食汁液，造成叶片卷缩、变形，植株生长受阻。分泌蜜露引起煤污病。",
        "advices": [
            "清除田间杂草，减少虫源",
            "保护利用天敌，如瓢虫、草蛉等",
            "发生初期喷施吡虫啉或啶虫脒",
            "可使用黄色粘虫板诱杀"
        ],
        "drugs": ["吡虫啉", "啶虫脒", "噻虫嗪", "高效氯氟氰菊酯"]
    },
    "红蜘蛛": {
        "symptoms": "主要为害叶片，以成螨、若螨在叶背吸食汁液，受害叶片出现黄白色小点，严重时叶片枯黄脱落。",
        "advices": [
            "及时清除田间杂草和枯枝落叶",
            "保护利用天敌，如捕食螨",
            "发生初期喷施阿维菌素或螺螨酯",
            "避免干旱，适当增加湿度"
        ],
        "drugs": ["阿维菌素", "螺螨酯", "哒螨灵", "联苯肼酯"]
    }
}


@router.post("/analyze", response_model=DiseaseAnalyzeResponse)
async def analyze_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """分析病虫害图片"""

    # 验证文件类型
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="请上传图片文件")

    # 保存图片
    upload_dir = "uploads/disease"
    os.makedirs(upload_dir, exist_ok=True)

    file_ext = os.path.splitext(file.filename)[1]
    file_name = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(upload_dir, file_name)

    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    # 模拟AI识别过程
    # 实际应用中这里会调用深度学习模型
    disease_names = list(DISEASE_DATABASE.keys())
    main_disease = random.choice(disease_names)

    # 生成置信度
    main_confidence = random.randint(75, 95)

    # 生成其他可能性
    other_diseases = [d for d in disease_names if d != main_disease]
    random.shuffle(other_diseases)
    other_possibilities = [
        {"name": other_diseases[0], "confidence": random.randint(3, 8)},
        {"name": other_diseases[1], "confidence": random.randint(1, 3)}
    ]

    disease_info = DISEASE_DATABASE[main_disease]

    # 保存记录
    record = DiseaseRecord(
        image_path=file_path,
        disease_name=main_disease,
        confidence=main_confidence,
        description=disease_info["symptoms"]
    )
    db.add(record)
    db.commit()

    return DiseaseAnalyzeResponse(
        name=main_disease,
        confidence=main_confidence,
        symptoms=disease_info["symptoms"],
        advices=disease_info["advices"],
        drugs=disease_info["drugs"],
        other_possibilities=other_possibilities
    )


@router.get("/history", response_model=List[DiseaseHistoryResponse])
def get_history(db: Session = Depends(get_db)):
    """获取识别历史"""
    records = db.query(DiseaseRecord).order_by(
        DiseaseRecord.created_at.desc()
    ).limit(20).all()

    return records
