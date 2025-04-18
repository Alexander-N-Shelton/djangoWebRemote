# remote/navigation_buttons.py

from remote.models import NavigationButton

navigation_buttons = [
    ('Home', 'fa-house', '3'),
    ('Up', 'fa-chevron-up', '19'),
    ('Power', 'fa-power-off', '177'),
    ('Back', 'fa-rotate-left', '4'),
    ('Left', 'fa-chevron-left', '21'),
    ('Down', 'fa-chevron-down', '20'),
    ('Right', 'fa-chevron-right', '22'),
    ('Enter', 'fa-check-double', '23')
]

for name, icon_class, keycode in navigation_buttons:
    NavigationButton.objects.get_or_create(
        name=name, 
        defaults={
            "icon_class": icon_class,
            "keycode": keycode
        }
    )