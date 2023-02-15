from form import Student
import sender

m_students = []


async def former(text):
    a = text.text.split(" ")
    if len(a) > 3:
        await text.answer("Слишком много, пиши согласно примеру:\n'Фамилия Имя Отчество'")
    elif len(a) < 3:
        await text.answer("Слишком мало, пиши согласно примеру:\n'Фамилия Имя Отчество'")
    else:
        m_students.append(Student(f"@{text.from_user.username}", a[1], a[0], a[2]))
        await text.answer("Ага, понятно.\nТеперь мне "
                          "нужно узнать твою группу. Напиши её в формате ХХ-ХХХ.\nПримеры:\nАК-127\nП-123")


async def group(text):
    a = text.text
    for i in m_students:
        if i.tg == f"@{text.from_user.username}":
            course = a.split("-")[1][0]
            i.group = a
            sender.creator(i)
            if course == "1":
                await text.answer("Отлично, будем знакомы!\nПрисоеденяйся к единомышленникам "
                                  "со своего курса!\n1 курс: t.me/+Q2YMMadMvzYwMWYy")
            elif course == "2":
                await text.answer("Отлично, будем знакомы!\nПрисоеденяйся к единомышленникам "
                                  "со своего курса!\n2 курс: t.me/+lPZahHRCD_xiZWRi")
            elif course == "3":
                await text.answer("Отлично, будем знакомы!\nПрисоеденяйся к единомышленникам "
                                  "со своего курса!\n3 курс: t.me/+7XtuePoTwws2MGQy")
            elif course == "4":
                await text.answer("Отлично, будем знакомы!\nПрисоеденяйся к единомышленникам "
                                  "со своего курса!\n4 курс: t.me/+yYq83Z3aJu4wMjFi")
            elif course == "5":
                await text.answer("Отлично, будем знакомы!\nПрисоеденяйся к единомышленникам "
                                  "со своего курса!\n5 курс: t.me/+BxNhyryhWtEyZDYy")
            elif course == "6":
                await text.answer("Отлично, будем знакомы!\nПрисоеденяйся к единомышленникам "
                                  "со своего курса!\n6 курс: t.me/+rOSx52zphLhiZGEy")
            m_students.remove(i)

