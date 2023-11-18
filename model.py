import torch.nn.functional as F
from torch import Tensor
from transformers import AutoTokenizer, AutoModel

def average_pool(last_hidden_states: Tensor,
                 attention_mask: Tensor) -> Tensor:
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]

input_texts = [
    """Ветеринарный врач
1. Осмотр животных и диагностирование их болезней и повреждений.
2. Исследование причин возникновения, процессов протекания болезней животных, разборку методов их лечения и профилактики.
3. Терапевтическое и хирургическое лечение животных.
4. Применение лекарственных средств при лечении животных, высокоэффективные ветеринарные препараты и методы ветеринарного воздействия.
5. Контроль выполнения зоогигиенических и ветеринарных правил при содержании, кормлении животных и уходе за ними на стационарном лечении.
6. Проведение ветеринарно-санитарной экспертизы скота 7. Осуществление руководства подчиненными ему работниками ветеринарного учреждения.""",

    """Ветеринарный врач
Выполнение ветеринарного законодательства. Контроль и своевременное выявление заболеваний. Профилактика и лечение.""",
    """Агроном
знание и умение выращивания посадочного материала, составление и видение технологического процесса выращивания продукции на протяжении года: обрезка, организация и контроль системы полива, мониторинг болезней и вредителей, подбор и внесение ядохимикатов.""",
    """Главный агроном
Разработка и внедрение технологий по борьбе с вредителями, болезнями растений и сорняками, разработка планов, календарных графиков по уходу за посевами."""
]

tokenizer = AutoTokenizer.from_pretrained("models")
model = AutoModel.from_pretrained("models")

# Tokenize the input texts
batch_dict = tokenizer(input_texts, max_length=512, padding=True, truncation=True, return_tensors='pt')

outputs = model(**batch_dict)
embeddings = average_pool(outputs.last_hidden_state, batch_dict['attention_mask'])
print(embeddings)

# (Optionally) normalize embeddings
embeddings = F.normalize(embeddings, p=2, dim=1)
scores = (embeddings[:1] @ embeddings[1:].T) * 100
print(scores.tolist())
