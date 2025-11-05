from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..relationship import Relationship
from ..filters.model import Filter


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
        answer_list = await filter_the_response(db, answer_list)
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


async def filter_the_response(
        db: AsyncSession,
        answer_list: list,
        /
) -> list[str]:
    query = select(Filter)
    result = await db.execute(query)
    filters = result.scalars().all()
    filter_length = len(filters)
    response_list = answer_list.copy()
    for i in range(filter_length):
        for j in range(len(answer_list)):
            if filters[i].label in answer_list[j]:
                a = answer_list[j].replace(filters[i].label, '')
                for k in range(len(answer_list)):
                    if filters[i].negative_label in answer_list[k] and a == answer_list[k].replace(filters[i].negative_label, ''):
                        response_list.remove(f'{a}{filters[i].label}')
    return response_list