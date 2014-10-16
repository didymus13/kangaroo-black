from django import template
from campaignManager.armies.models import Game
register = template.Library()

class GameLinksNode(template.Node):
    def __init__(self, url_string):
        self.url_string = template.Variable(url_string)
    
    def render(self, context):
        path = self.url_string.resolve(context)
        try:
            games = Game.objects.all()
        except:
            # Fail silently if no games created
            games = ()
        output = ''
        for game in games:
            output += "<li><a href='%s%s'>%s</a></li>" % (path, game.slug, game.name)
        return output

@register.tag(name="game_links")
def do_game_links(parser, token):
    try:
        tag_name, url_string = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    
    return GameLinksNode(url_string)