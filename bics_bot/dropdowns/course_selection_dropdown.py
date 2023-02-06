from bics_bot.embeds.courses_embed import CoursesSelectionEmbed
import nextcord
import json

PATH = "./bics_bot/data/discord_channels.json"

with open(PATH) as f:
    text_channels = json.load(f)


class DropdownItem1(nextcord.ui.Select):
    def __init__(self, enrolled_courses):
        super().__init__(
            placeholder="Year 1",
            min_values=0,
            max_values=len(self._get_options(enrolled_courses)),
            options=self._get_options(enrolled_courses),
        )

    def _get_options(self, enrolled_courses):
        options = []
        enrolled = False
        for value in text_channels["courses"]["year1"]["winter"]:
            if value["name"] in enrolled_courses:
                enrolled = True
            else:
                enrolled = False
            options.append(
                nextcord.SelectOption(
                    label=value["name"], description="Semester 1 course", emoji="⛄", default=enrolled
                )
            )
        for value in text_channels["courses"]["year1"]["summer"]:
            if value["name"] in enrolled_courses:
                enrolled = True
            else:
                enrolled = False
            options.append(
                nextcord.SelectOption(
                    label=value["name"], description="Semester 2 course", emoji="☀️", default=enrolled
                )
            )
        return options


class DropdownItem2(nextcord.ui.Select):
    def __init__(self, enrolled_courses):
        super().__init__(
            placeholder="Year 2",
            min_values=0,
            max_values=len(self._get_options(enrolled_courses)),
            options=self._get_options(enrolled_courses),
        )

    def _get_options(self, enrolled_courses):
        options = []
        enrolled = False
        for value in text_channels["courses"]["year2"]["winter"]:
            if value["name"] in enrolled_courses:
                enrolled = True
            else:
                enrolled = False
            options.append(
                nextcord.SelectOption(
                    label=value["name"], description="Semester 3 course", emoji="⛄", default=enrolled
                )
            )
        for value in text_channels["courses"]["year2"]["summer"]:
            if value["name"] in enrolled_courses:
                enrolled = True
            else:
                enrolled = False
            options.append(
                nextcord.SelectOption(
                    label=value["name"], description="Semester 4 course", emoji="☀️", default=enrolled
                )
            )
        return options


class DropdownItem3(nextcord.ui.Select):
    def __init__(self, enrolled_courses):
        self.chosen_options = []
        super().__init__(
            placeholder="Year 3",
            min_values=0,
            max_values=len(self._get_options(enrolled_courses)),
            options=self._get_options(enrolled_courses),
        )

    def _get_options(self, enrolled_courses):
        options = []
        enrolled = False
        for value in text_channels["courses"]["year3"]["winter"]:
            if value["name"] in enrolled_courses:
                enrolled = True
            else:
                enrolled = False
            options.append(
                nextcord.SelectOption(
                    label=value["name"], description="Semester 5 course", emoji="⛄", default=enrolled
                )
            )
        for value in text_channels["courses"]["year3"]["summer"]:
            if value["name"] in enrolled_courses:
                enrolled = True
            else:
                enrolled = False
            options.append(
                nextcord.SelectOption(
                    label=value["name"], description="Semester 6 course", emoji="☀️", default=enrolled
                )
            )
        return options


class DropdownView(nextcord.ui.View):
    def __init__(self, enrolled_courses: list[str]):
        super().__init__()
        self.item1 = DropdownItem1(enrolled_courses)
        self.item2 = DropdownItem2(enrolled_courses)
        self.item3 = DropdownItem3(enrolled_courses)
        self.add_item(self.item1)
        self.add_item(self.item2)
        self.add_item(self.item3)

    @nextcord.ui.button(label="Confirm", style=nextcord.ButtonStyle.green, row=3)
    async def confirm_callback(
        self, button: nextcord.Button, interaction: nextcord.Interaction
    ):
        _courses = [self.item1.values, self.item2.values, self.item3.values] #list with year data
        courses = {} #dict without year data
        for course in _courses:
            courses[tuple(course)] = True
        embed = CoursesSelectionEmbed(courses)
        await self.give_course_permissions(courses, interaction.user, interaction.guild)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        self.stop()

    @nextcord.ui.button(
        label="Cancel", style=nextcord.ButtonStyle.red, row=3, custom_id="cancel-btn"
    )
    async def cancel_callback(
        self, button: nextcord.Button, interaction: nextcord.Interaction
    ):
        await interaction.response.send_message("Canceled operation. No changes made.", ephemeral=True)
        self.stop()

    async def give_course_permissions(self, courses: dict[str], user: nextcord.Interaction.user, guild: nextcord.Guild):
        for text_channel in guild.text_channels:
            if self.is_enrollable(courses, text_channel, user):
                await text_channel.set_permissions(target=user, read_messages=True,
                                                    send_messages=True)
            elif self.is_unenrollable(courses, text_channel, user):
                await text_channel.set_permissions(target=user, read_messages=False,
                                                    send_messages=False)

    def is_course_channel(self, category_id):  # from left to right: sem6-1
        return category_id == 985956666971402240 or category_id == 985956596414808105 or category_id == 939222837082865725 or category_id == 860599769940361267 or category_id == 889981953934254101 or category_id == 755869390951677992
    
    def is_enrollable(self, courses:dict[str], channel:nextcord.TextChannel, user:nextcord.Interaction.user):
        return courses.get(channel.name) and not channel.permissions_for(user).read_messages

    def is_unenrollable(self, courses:dict[str], channel:nextcord.TextChannel, user:nextcord.Interaction.user):
        return courses.get(channel.name) and channel.permissions_for(user).read_messages