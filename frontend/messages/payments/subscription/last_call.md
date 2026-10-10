(придумано ИИ, TODO заменить) Здравствуйте, {{ user.full_name }}!

Срок вашего членства давно закончился, и сейчас мы удаляем вас из клубных Telegram-чатов. Аккаунт и профиль останутся на месте.
{% if rooms %}
Вот чаты, из которых вас удалят: {% for room in rooms|slice:":20" %}{% if room.icon %}{{ room.icon }} {% endif %}{{ room.chat_name }}{% if not forloop.last %}, {% endif %}{% endfor %}.
{% endif %}
Если хотите остаться, продлите членство. Доступ восстановится, и в чаты можно будет вернуться:

[.button.button-big Восстановить доступ]({{ settings.APP_HOST }}{% url "edit_payments" user.slug %})

Спасибо, что были с нами. Будем рады видеть вас снова 🖤
