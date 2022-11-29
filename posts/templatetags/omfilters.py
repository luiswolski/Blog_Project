from django import template

register = template.Library()


@register.filter(name='plural_comments')
def plural_comments(num_comments):
    try:
        num_comments = int(num_comments)

        if num_comments == 0:
            return f'No comments yet'
        elif num_comments == 1:
            return f'{num_comments} comment'
        else:
            return f'{num_comments} comments'
    except:
        return f'{num_comments} comment(s)'
