from lxml import html
import urwid
import urllib.request

my_hashtags = ['CTF', 'Django', 'Flask', 'I2P', 'IT-инфраструктура',
               'Python', 'SQL', 'Антивирусная защита', 'Будущее здесь',
               'Высокая производительность', 'Гаджеты',
               'Информационная безопасность', 'Компьютерное железо',
               'Криптография', 'Научно-популярное', 'Отладка',
               'Программирование',
               'Промышленное программирование', 'Робототехника',
               'Спам и антиспам']


def parse():
    links = []
    for i in range(1, 5):
        url = 'https://habr.com/ru/all/page{0}/'.format(i)

        request_html = urllib.request.urlopen(url)
        mybytes = request_html.read()
        # req = mybytes.decode("utf8")
        # request_html.close()

        tree = html.fromstring(mybytes)  # Можно заменить на mybytes
        link = tree.xpath('//*[@id]/article/h2/a/@href')
        for article in link:
            links.append(article)
    return links
    # text = tree.xpath('//*[@id]/article/h2/a/text()')


def parse_article(links):
    art = {}
    for url in links:
        request_html = urllib.request.urlopen(url)
        mybytes = request_html.read()
        tree = html.fromstring(mybytes)
        hashtags = tree.xpath('//*[@id]/div/ul/li/a/text()')
        article_name = tree.xpath('//*[@id]/div/h1/span/text()')
        if list(set(hashtags) & set(my_hashtags)):
            # for hashtag in hashtags:
            # if hashtag in my_hashtags:
            art[article_name[0]] = url
    return art


def menu_button(caption, callback, data=None):
    if data:
        button = urwid.Button(caption)
        urwid.connect_signal(button, 'click', callback, data)
        return urwid.AttrMap(button, None, focus_map='reversed')
    else:
        button = urwid.Button(caption)
        urwid.connect_signal(button, 'click', callback)
        return urwid.AttrMap(button, None, focus_map='reversed')


def sub_menu(caption, choices):
    contents = menu(caption, choices)

    def open_menu(button):
        return top.open_box(contents)

    return menu_button([caption, u'...'], open_menu)


def menu(title, choices):
    body = [urwid.Text(title), urwid.Divider()]
    body.extend(choices)
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))



def item_chosen(button, choice):
    response = urwid.Text([u'You chose ', choice, u'\n'])
    done = urwid.Button(u'Press ESC to return, ENTR to exit')
    urwid.connect_signal(done, 'click', open_url(choice))
    top.open_box(urwid.Filler(urwid.Pile([response, done])))


def open_url(button):
    import webbrowser
    webbrowser.open(button)
    # raise urwid.ExitMainLoop()


# content = parse_article(parse())
## for key, value in content.items():
# menu(key, [menu_button(value, item_chosen)])
# menu_top = menu('Habroparser',[menu_button('tata', item_chosen)])
# 'menu_button(u'Terminal', item_chosen)'
# menu_top = menu('Habroparser',[menu_button('Cylance против Sality',
# item_chosen,'ass')])
def make(articles: dict):
    menu_to_eval = ""
    for key, value in list(articles.items())[0:1]:
        menu_to_eval += "menu('Habraparser',[sub_menu('{0}',[menu_button('{" \
                        "1}', item_chosen,'{1}')]),".format(key,
                                                            value).replace(
            '//', '/')
    for key, value in list(articles.items())[1:len(articles) - 1]:
        # menu_button(u'Terminal', item_chosen),
        menu_to_eval += "sub_menu('{0}',[menu_button('{1}', item_chosen," \
                        "'{1}')]),".format(key,
                                           value).replace(
            '//', '/')
    for key, value in list(articles.items())[len(articles) - 1:len(articles)]:
        menu_to_eval += "sub_menu('{0}',[menu_button('{" \
                        "1}', item_chosen,'{1}')])])".format(key,
                                                             value).replace(
            '//', '/')
    return menu_to_eval


class CascadingBoxes(urwid.WidgetPlaceholder):
    max_box_levels = 4

    def __init__(self, box):
        super(CascadingBoxes, self).__init__(
            urwid.SolidFill(u'\N{MEDIUM SHADE}'))
        self.box_level = 0
        self.open_box(box)

    def open_box(self, box):
        self.original_widget = urwid.Overlay(urwid.LineBox(box),
                                             self.original_widget,
                                             align='center',
                                             width=('relative', 95),
                                             valign='middle',
                                             height=('relative', 92),
                                             min_width=20, min_height=8)
        self.box_level += 1

    def keypress(self, size, key):
        if key == 'esc' and self.box_level > 1:
            self.original_widget = self.original_widget[0]
            self.box_level -= 1
        else:
            return super(CascadingBoxes, self).keypress(size, key)


# main = urwid.Padding(menu(u'Pythons', parse_article(parse())), left=2,
# right=5)

top = CascadingBoxes(eval(make(parse_article(parse()))))
try:
    urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()
except KeyboardInterrupt:
    urwid.ExitMainLoop()
except TypeError:
    urwid.ExitMainLoop()
