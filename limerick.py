import random

LIMERICK_TEMPLATE = (
    'Молодой человек {birthplace}\n'
    'Как-то {action1} {action2},\n'
    'А минут через двадцать {after_action1} {after_action2}.\n'
    'Хоть {post_action}.'
)
BIRTHPLACES = [
    'из Ростова',
    'из-под Пскова',
    'из Коврова',
    'из Тамбова',
    'из Сарова',
    'из Венёва',
]
ACTIONS1 = [
    'слушал полдня',
    'в школу принёс',
    'видел в пруду',
    'съел на обед',
    'спас от дождя',
]
ACTIONS2 = [
    'рыболова',
    'две подковы',
    'водяного',
    'хвост коровы',
    'миску плова',
]
AFTER_ACTIONS1 = [
    'постеснялся',
    'стал ржать и',
    'побоялся',
    'стал уныло',
]
AFTER_ACTIONS2 = [
    'смеяться',
    'лягаться',
    'купаться',
    'болтаться',
]
POST_ACTIONS = [
    'потом не поверил ни слову',
    'вреда не нанёс никакого',
    'совсем и не думал плохого',
    'остался живым и здоровым',
    'не видел варианта иного',
]


def compose_limerick() -> str:
    limerick = LIMERICK_TEMPLATE.format(
        birthplace=random.choice(BIRTHPLACES),
        action1=random.choice(ACTIONS1),
        action2=random.choice(ACTIONS2),
        after_action1=random.choice(AFTER_ACTIONS1),
        after_action2=random.choice(AFTER_ACTIONS2),
        post_action=random.choice(POST_ACTIONS),
    )
    return limerick
