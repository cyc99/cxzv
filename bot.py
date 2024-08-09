import discord
from secrets import TOKEN
from discord.ext.commands import Bot
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True
# 사용자가 명령어 입력 시 ./를 입력하고 명령어 입력
client = Bot(command_prefix='/', intents=intents)
tree = client.tree

class PageButton(discord.ui.Button):
  def __init__(self, page_data, arrow_type, emoji_list, size):
      self.emoji_list = emoji_list
      self.page_data = page_data
      self.arrow_type = arrow_type
      self.size = size
      label = '◀' if arrow_type == 1 else '▶'
      disabled = False
      if (page_data[2] == 0 and arrow_type == 1) or (page_data[2] == page_data[1] and arrow_type == 0):
        style = discord.ButtonStyle.grey
        disabled = True
      else:
        style = discord.ButtonStyle.green
      super().__init__(label=label, style=style, disabled=disabled, row=0)
      
  async def callback(self, interaction):
      view = discord.ui.View()
      if self.arrow_type == 1:
          self.page_data[2] = self.page_data[2] - 1
      else:
          self.page_data[2] = self.page_data[2] + 1
      view.add_item(PageButton(self.page_data[:], 1, self.emoji_list, self.size))
      view.add_item(PageButton(self.page_data[:], 0, self.emoji_list, self.size))
      indices = len(self.emoji_list) % 20 if self.page_data[2] == self.page_data[1] else 20
      for i in range(indices):
          view.add_item(EmojiButton(self.emoji_list[self.page_data[2] * 20 + i], self.size, (i // 5) + 1))
      await interaction.response.edit_message(view=view)
      
      

class EmojiButton(discord.ui.Button):
  
  def __init__(self, emojier, size=None, row=None):
    self.emojier = emojier
    self.size = size
    super().__init__(emoji=emojier, style=discord.ButtonStyle.grey, row=row)
      
  async def callback(self, interaction):
    author = interaction.user
    size = self.size if self.size else 128
    embed = discord.Embed()
    embed.set_image(url=self.emojier.url + f'?size={size}')
    embed.set_author(name=author.display_name)
    await interaction.response.send_message(embed=embed)
    
async def setup_hook():
  await client.tree.sync()

# on_ready는 시작할 때 한번만 실행.
@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online, activity=discord.Game('이모지 돚거'))
  print('done')
  

    
# 아래 코드들은 client.event의 on_message를 주석 처리하고 실행
# @client.tree.command(description='이모지 목록을 버튼으로 보여줍니다.')
# async def asdf(interaction, size: int=128):
#   emojis = list(interaction.context.message.guild.emojis)
#   pages = (len(emojis) // 25) + 1
#   for page in range(pages):
#     view = discord.ui.View()
#     indices = len(emojis) % 25 if page == pages-1 else 25
#     for i in range(indices):
#         view.add_item(EmojiButton(emojis[page * 25 + i], size))
#     await interaction.response.send_message(view=view, ephemeral=True, delete_after=20.0)

@client.tree.command(name='1', description='이모지 돚거 목록을 보여줍니다.')
@app_commands.choices(choices=[
    app_commands.Choice(name='16', value=16),
    app_commands.Choice(name='32', value=32),
    app_commands.Choice(name='64', value=64),
    app_commands.Choice(name='128', value=128),
    app_commands.Choice(name='256', value=256),
    app_commands.Choice(name='512', value=512),
    app_commands.Choice(name='1024', value=1024),
])
async def asdf(interaction, choices: app_commands.Choice[int]):
#   ctx = interaction.context
  emojis = list(interaction.guild.emojis)
  pages = (len(emojis) // 20)
  view = discord.ui.View()
  view.add_item(PageButton([0, pages, 0], 1, emojis, choices.value))
  view.add_item(PageButton([0, pages, 0], 0, emojis, choices.value))
  indices = len(emojis) % 20 if pages == 0 else 20
  for i in range(indices):
    view.add_item(EmojiButton(emojis[i], choices.value, (i // 5) + 1))
  await interaction.response.send_message(view=view, ephemeral=True, delete_after=60.0)


client.setup_hook = setup_hook
client.run(TOKENs)