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
    for i in range(length):
        if label == relationships[i].node1.label:
            answer_list.append(f'{relationships[i].node2.label} {relationships[i].edge.label}')
            await verify_nested_nodes(relationships[i].node2_id, relationships, length, answer_list)
    return answer_list


async def verify_nested_nodes(node_id, relationships: list, length: int, answer_list, /):
    for i in range(length):
        if relationships[i].node1.id == node_id:
            answer_list.append(f'{relationships[i].node2.label} {relationships[i].edge.label}')
            await verify_nested_nodes(node_id, relationships, length, answer_list)
