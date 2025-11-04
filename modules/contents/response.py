from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..relationship import Relationship


async def answer_to_question(
        db: AsyncSession,
        label: str,
        /
) -> list[str]:
    query = select(Relationship)
    result = await db.execute(query)
    relationships = result.scalars().all()
    # asosiy malumotlarni olish
    length = len(relationships)
    answer_list = []
    # aynan moslik bilan tekshirish
    for i in range(length):
        if label == relationships[i].node1.label.lower():
            answer_list.append(f'{relationships[i].node2.label} {relationships[i].edge.label}')
            await verify_nested_nodes(relationships[i].node2_id, relationships, length, answer_list)
    if answer_list:
        return answer_list
    await to_form_analogies(label, relationships, length, answer_list)
    if not answer_list:
        answer_list = ['Javob uchun malumot topilmadi']
    return answer_list


async def verify_nested_nodes(node_id, relationships: list, length: int, answer_list, /):
    for i in range(length):
        if relationships[i].node1.id == node_id:
            answer_list.append(f'{relationships[i].node2.label} {relationships[i].edge.label}')
            await verify_nested_nodes(relationships[i].node2_id, relationships, length, answer_list)


async def to_form_analogies(
        label: str,
        relationships: list,
        length: int,
        answer_list: list,
        /
) -> list[str]:
    answer_list.append('Siz shulardan qaysi birini nazarda tutdingiz')
    for i in range(length):
        if label in relationships[i].node1.label.lower():
            if answer_list != []:
                if not relationships[i].node1.label in answer_list:
                    answer_list.append(relationships[i].node1.label)
            else:
                answer_list.append(relationships[i].node1.label)