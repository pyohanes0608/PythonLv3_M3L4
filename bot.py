import discord
from discord.ext import commands
from logic import DB_Manager
from config import DATABASE, TOKEN

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)
manager = DB_Manager(DATABASE)

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')

@bot.command(name='start')
async def start_command(ctx):
    await ctx.send("Halo! Saya adalah bot pengelola proyek\nSaya akan membantumu menyimpan proyek-proyekmu beserta informasinya! =)")
    await info(ctx)

@bot.command(name='info')
async def info(ctx):
    await ctx.send("""
Berikut adalah perintah-perintah yang bisa kamu gunakan:

!new_project - menambah proyek baru
!projects - melihat daftar semua proyekmu
!update_projects - mengubah data proyek
!skills - menghubungkan kemampuan dengan proyek tertentu
!delete - menghapus proyek

Kamu juga bisa mengetik nama proyek untuk melihat semua informasi tentang proyek tersebut!""")

@bot.command(name='new_project')
async def new_project(ctx):
    await ctx.send("Silakan masukkan nama proyek")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    name = await bot.wait_for('message', check=check)
    data = [ctx.author.id, name.content]
    await ctx.send("Silakan kirim link proyek")
    link = await bot.wait_for('message', check=check)
    data.append(link.content)

    statuses = [x[0] for x in manager.get_statuses()]
    await ctx.send("Silakan masukkan status terkini dari proyek", delete_after=60.0)
    await ctx.send("\n".join(statuses), delete_after=60.0)
    
    status = await bot.wait_for('message', check=check)
    if status.content not in statuses:
        await ctx.send("Status yang kamu pilih tidak ada dalam daftar. Silakan coba lagi!", delete_after=60.0)
        return

    status_id = manager.get_status_id(status.content)
    data.append(status_id)
    manager.insert_project([tuple(data)])
    await ctx.send("Proyek telah berhasil disimpan")

@bot.command(name='projects')
async def get_projects(ctx):
    user_id = ctx.author.id
    projects = manager.get_projects(user_id)
    if projects:
        text = "\n".join([f"Nama proyek: {x[2]} \nLink: {x[4]}\n" for x in projects])
        await ctx.send(text)
    else:
        await ctx.send('Kamu belum memiliki proyek!\nMau coba tambah proyek dengan perintah !new_project?')

@bot.command(name='skills')
async def skills(ctx):
    user_id = ctx.author.id
    projects = manager.get_projects(user_id)
    if projects:
        projects = [x[2] for x in projects]
        await ctx.send('Pilih proyek yang ingin kamu hubungkan dengan kemampuan')
        await ctx.send("\n".join(projects))

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        project_name = await bot.wait_for('message', check=check)
        if project_name.content not in projects:
            await ctx.send('Kamu tidak memiliki proyek ini, silakan coba lagi! Pilih proyek yang ingin kamu hubungkan dengan kemampuan')
            return

        skills = [x[1] for x in manager.get_skills()]
        await ctx.send('Pilih kemampuan')
        await ctx.send("\n".join(skills))

        skill = await bot.wait_for('message', check=check)
        if skill.content not in skills:
            await ctx.send('Sepertinya kemampuan yang kamu pilih tidak ada dalam daftar! Silakan coba lagi! Pilih kemampuan')
            return

        manager.insert_skill(user_id, project_name.content, skill.content)
        await ctx.send(f'Kemampuan {skill.content} telah terhubung dengan proyek {project_name.content}')
    else:
        await ctx.send('Kamu belum memiliki proyek!\nMau coba tambah proyek dengan perintah !new_project?')

@bot.command(name='delete')
async def delete_project(ctx):
    user_id = ctx.author.id
    projects = manager.get_projects(user_id)
    if projects:
        projects = [x[2] for x in projects]
        await ctx.send("Pilih proyek yang ingin kamu hapus")
        await ctx.send("\n".join(projects))

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        project_name = await bot.wait_for('message', check=check)
        if project_name.content not in projects:
            await ctx.send('Kamu tidak memiliki proyek ini, silakan coba lagi!')
            return

        project_id = manager.get_project_id(project_name.content, user_id)
        manager.delete_project(user_id, project_id)
        await ctx.send(f'Proyek {project_name.content} telah dihapus dari database!')
    else:
        await ctx.send('Kamu belum memiliki proyek!\nMau coba tambah proyek dengan perintah !new_project?')

@bot.command(name='update_projects')
async def update_projects(ctx):
    user_id = ctx.author.id
    projects = manager.get_projects(user_id)
    if projects:
        projects = [x[2] for x in projects]
        await ctx.send("Silakan pilih proyek yang ingin kamu perbarui")
        await ctx.send("\n".join(projects))

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        project_name = await bot.wait_for('message', check=check)
        if project_name.content not in projects:
            await ctx.send("Ada yang salah! Silakan pilih lagi proyek yang ingin kamu ubah:")
            return

        await ctx.send("Apa yang ingin kamu ubah dari proyek ini?")
        attributes = {'Nama proyek': 'project_name', 'Deskripsi': 'description', 'Link proyek': 'url', 'Status proyek': 'status_id'}
        await ctx.send("\n".join(attributes.keys()))

        attribute = await bot.wait_for('message', check=check)
        if attribute.content not in attributes:
            await ctx.send("Ups, ada kesalahan! Silakan coba lagi!")
            return

        if attribute.content == 'Status':
            statuses = manager.get_statuses()
            await ctx.send("Silakan pilih status baru untuk proyekmu")
            await ctx.send("\n".join([x[0] for x in statuses]))
            update_info = await bot.wait_for('message', check=check)
            if update_info.content not in [x[0] for x in statuses]:
                await ctx.send("Status yang dipilih tidak sesuai, silakan coba lagi!")
                return
            update_info = manager.get_status_id(update_info.content)
        else:
            await ctx.send(f"Masukkan data baru untuk {attribute.content}")
            update_info = await bot.wait_for('message', check=check)
            update_info = update_info.content

        manager.update_projects(attributes[attribute.content], (update_info, project_name.content, user_id))
        await ctx.send("Selesai! Proyek telah diperbarui!")
    else:
        await ctx.send('Kamu belum memiliki proyek!\nMau coba tambah proyek dengan perintah !new_project?')

bot.run(TOKEN)
