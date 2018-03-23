from django import template

register = template.Library()

@register.filter
def only_my_note(notes, my_user):
    return notes.filter(user=my_user)

@register.filter
def only_my_answer(answers, my_user):
    return answers.filter(user=my_user)

@register.filter
def prayer_topics(cards, pp):
    return cards.filter(card_type__name=pp)

@register.filter
def book(scriptures, book_name):
    return scriptures.filter(book=book_name)
