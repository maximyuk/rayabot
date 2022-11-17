import discord
import asyncio
import random
from discord.ext import commands, tasks
from discord.ext.commands import bot
from config import settings
import pymysql
import pymysql.cursors
import json
import requests



bot = commands.Bot(command_prefix = settings['prefix'], intents=discord.Intents.all()) # Так как мы указали префикс в settings, обращаемся к словарю с ключом prefix.    
bot.remove_command( 'help' )

#---------------------------------------------------------utils----------------------------------------------------------------------------------------------
try:
    connect = pymysql.connect(host='localhost', user='root', password='root',
                              charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)  # подключення до бд
    cursor = connect.cursor()
    try:
        # тіп створює бд
        cursor.execute("CREATE DATABASE IF NOT EXISTS rayabot")
    finally:
        connect.commit()
except Exception as ex:
    print(ex)
 
 


#---------------------------------------------------цей евентс означає коли бот добавляється на сервер-------------------------------------------------------------------------------------------
@bot.event
async def on_guild_join(guild):
    mrole = discord.utils.get(guild.roles, name="Mute by Raya")
    vmrole = discord.utils.get(guild.roles, name="VMute by Raya")

    if mrole not in guild.roles:
        await guild.create_role(name="Mute by Raya")
    if vmrole not in guild.roles:
        await guild.create_role(name="VMute by Raya")
    else:
        print('Ролі вже створені')

#----------------------------------------------------------создає таблицю узерс коли бот добавляється на сервер----------------------------------------------------------------------------------------------------
    try:
        cursor.execute(f"create table if not exists rayabot.users(guild_name varchar(50), user_name varchar(50),guild int default null, user_id int default null, mute int default null, ban int default null, warn int default null, admin int default null)")  # создає таблицю
    except Exception as ex:
        print(ex)
    finally:
        connect.commit()
 
    for guild in bot.guilds:
        for member in guild.members:
            cursor.execute(f"select * from rayabot.users where guild = {guild.id} and user_id = {member.id}")
            if cursor.fetchone() is None:
                cursor.execute(f"insert into rayabot.users values('{member.guild.name}', '{member}',{member.guild.id}, {member.id}, 0, 0, 0, 0)")
                connect.commit()
            else:
                print('\u200b')

    cursor.execute(f"UPDATE rayabot.users SET admin = 6 WHERE guild = {guild.id} AND user_id = {guild.owner.id}")
    connect.commit()


#--------------------------------------------------------------создає таблицю guilds коли бот добавляється на сервер-----------------------------------------------------------------------
    try:
        cursor.execute(f"create table if not exists rayabot.guilds(guild_name varchar(50) , guild_id bigint default null, welcome text)")  # создає таблицю
    except Exception as ex:
        print(ex)
    finally:
        connect.commit()
 
    for guild in bot.guilds:
        for member in guild.members:
            cursor.execute(f"select * from rayabot.guilds where guild_name = '{guild.name}' and guild_id = {guild.id}")
            if cursor.fetchone() is None:
                cursor.execute(f"insert into rayabot.guilds values('{member.guild.name}', {member.guild.id}, NOT NULL)")
                connect.commit()
            else:
                print('\u200b')
    








#-------------------------------------------------------------------------------прогрузка бота + статус бота--------------------------------------------------------------------
 
@bot.event
async def on_ready():
    # статус
    while True:
        await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.listening, name="https://rayabot.tk")) #статус
        await asyncio.sleep(10)
        await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.playing , name="Обновление 0.2"))
        await asyncio.sleep(10)

    print('======================================')
    print('')
    print('Loading.')
    print('Loading..')
    print('Loading...')
    print('Loading: 16%')
    print('Loading: 48%')
    print('Loading: 50%')
    print('Loading: 87%')
    print('Loading: 100%')
    print('Bot status: online')
    print('')
    print('======================================')



 #-------------------------------------------------------------------создає таблицю users коли бот включається-------------------------------------------------------------------
    try:
        cursor.execute(f"create table if not exists rayabot.users(guild_name varchar(33), user_name varchar(33),guild bigint default null, user_id bigint default null, mute int default null, ban int default null, warn int default null, admin int default null)")  # создає таблицю
    except Exception as ex:
        print(ex)
    finally:
        connect.commit()
 
    for guild in bot.guilds:
        for member in guild.members:
            cursor.execute(f"select * from rayabot.users where guild = {guild.id} and user_id = {member.id}")
            if cursor.fetchone() is None:
                cursor.execute(f"insert into rayabot.users values('{member.guild.name}', '{member}',{member.guild.id}, {member.id}, 0, 0, 0, 0)")
                connect.commit()
            else:
                print('\u200b')

        cursor.execute(f"UPDATE rayabot.users SET admin = 6 WHERE guild = {guild.id} AND user_id = {guild.owner.id}")
        connect.commit()
#-------------------------------------------------------------Создає таблицю guilds коли бот включається-------------------------------------------------------------------

    try:
        cursor.execute(f"create table if not exists rayabot.guilds(guild_name varchar(50), guild_id bigint default null, welcome text default null)")  # создає таблицю
    except Exception as ex:
        print(ex)
    finally:
        connect.commit()
 
    for guild in bot.guilds:
        cursor.execute(f"select * from rayabot.guilds where guild_name = '{guild.name}' and guild_id = {guild.id}")
        if cursor.fetchone() is None:
            cursor.execute(f"insert into rayabot.guilds(guild_name, guild_id) values('{guild.name}' , {guild.id})")
            connect.commit()
        else:
            print('\u200b')



#--------------------------------------------------------------------добавляє всю інфу в users про чела коли він заходить на сервер-----------------------------------------------------
 
@bot.event
async def on_member_join(member):
    cursor.execute(f"select * from rayabot.guilds where guild_id = {member.guild.id}")
    welcomes = cursor.fetchone()['welcome']
    if welcomes == None:
        pass
    else:
        embed=discord.Embed(title=":smiley: Приветствие участника", description=f'▹ {welcomes} ', color= 0x008080)
        await member.send(embed=embed)




    for member in member.guild.members:
        cursor.execute(f"select guild, user_id from rayabot.users where guild = {member.guild.id} and user_id = {member.id}")
        if cursor.fetchone() is None:
            cursor.execute(f"insert into rayabot.users values('{member.guild.name}', '{member}',{member.guild.id}, {member.id}, 0, 0, 0, 0)")
            connect.commit()
        else:
            print('\u200b')

#-------------------------------------------------------------------Добававляє всю інфу в guilds коли чел заходить на сервер----------------------------------------------
    for member in member.guild.members:
        cursor.execute(f"select guild_name ,guild_id from rayabot.guilds where guild_name = '{member.guild.name}' and guild_id = {member.guild.id}")
        if cursor.fetchone() is None:
            cursor.execute(
                f"insert into rayabot.guilds values({member.guild.id} ,{member.guild.id}, NOT NULL)")
            connect.commit()
        else:
            print('\u200b')




@bot.event
async def on_member_remove(member):
    cursor.execute(
        f"update rayabot.users set admin = 0 where user_id = {member.id} and guild = {member.guild.id}")
    connect.commit()
#--------------------------------------------------------warn--------------------------------------------------------------------------------------------

@bot.command()
async def warn(ctx, user: discord.Member, count: int, *, reason = None):
    cursor.execute(f"select * from rayabot.users where guild = '{ctx.guild.id}' and user_id = '{ctx.message.author.id}'")
    _admin = cursor.fetchone()['admin']
    cursor.execute(f"select * from rayabot.users where guild = '{ctx.guild.id}' and user_id = '{user.id}'")
    admins = cursor.fetchone()['admin']
    if _admin <4:
        emb4 = discord.Embed(title=" Что-то пошло не так ",  description= f'\n▹ Упс, у вас не недостаточно прав ', color=0xff9900)
        emb4.set_footer(text=f'Отправлено: {ctx.author}  | Тест бот (c) 2022 •   ', icon_url=ctx.author.avatar_url,  )
        message = await ctx.send(embed = emb4)
    else:
        if _admin < admins:
            embed=discord.Embed(title=f'Что-то пошло не так', description=f'Вы не можете взаемодействовать с пользователем у которого уровень администратора выше вашего! ', color= 0xffff00)
            await ctx.send(embed=embed)
        else:
            cursor.execute(f"select * from rayabot.users where guild = '{ctx.guild.id}' and user_id = '{user.id}'")
            warns = cursor.fetchone()['warn']
            if count >3:
                embed7 = discord.Embed(title="Ошибка", description=f"К сожелению максимальное количество предупреждений `3` дальше пользователь получит *блокировку на данном сервере*", color=0x008080)
                await ctx.reply(embed=embed7)
            if count <=0:
                embed7 = discord.Embed(title="Ошибка", description=f"Значение должно быть больше/равно `1` ", color=0x008080)
                await ctx.reply(embed=embed7)

            if count >3:
                embed7 = discord.Embed(title="Примітка!", description=f"Нажаль, максимальна кількість попереджень `3` а потім `БАН`🦆", color=0x008080)
                await ctx.reply(embed=embed7)
            else:
                if warns >= 3: 
                    embed7 = discord.Embed(title="Примітка!", description=f"Нажаль, максимальна кількість попереджень повинно бути `3`🦆", color=0x008080)
                    await ctx.reply(embed=embed7)
                else:
                    if count == 1:
                        if warns == 0:
                            cursor.execute(f"update rayabot.users set warn = warn + 1 where user_id = '{user.id}'")
                            connect.commit()
                            embed=discord.Embed(title=f'Вам выдали `1` предупреждение на сервере `{ctx.guild.name}`', description=f'Модератором {ctx.message.author.mention}', color= 0x008080)
                            embed.add_field(name='Причина:', value=f'{reason}', inline=True)
                            await user.send(embed=embed)
                        
                            embed1=discord.Embed(title= 'Успешное выполнение команды:' , description=f'Пользователю {user.mention} было выдано `1` предупреждение', color=0x008080)
                            embed1.add_field(name='Задачу выполнил:', value=f'{ctx.message.author.mention}', inline=True)
                            embed1.add_field(name='Причина:', value=f'{reason}', inline=True)
                            embed1.add_field(name='Количество:', value=f"1/3")
                            await ctx.send(embed=embed1)
                        if warns == 1:
                            cursor.execute(f"update rayabot.users set warn = warn + 1 where user_id = '{user.id}' and guild = '{ctx.guild.id}'")
                            connect.commit()
                            embed=discord.Embed(title=f'Вам выдали `1` предупреждение на сервере `{ctx.guild.name}`', description=f'Модератором {ctx.message.author.mention}', color= 0x008080)
                            embed.add_field(name='Причина:', value=f'{reason}', inline=True)
                            await user.send(embed=embed)
                        
                            embed1=discord.Embed(title= 'Успешное выполнение команды:' , description=f'Пользователю {user.mention} было выдано `1` предупреждение', color=0x008080)
                            embed1.add_field(name='Задачу выполнил:', value=f'{ctx.message.author.mention}', inline=True)
                            embed1.add_field(name='Причина:', value=f'{reason}', inline=True)
                            embed1.add_field(name='Количество:', value=f"2/3")
                            await ctx.send(embed=embed1)
                        if warns == 2:
                            embed=discord.Embed(title=f'Вам выдали `1` предупреждение на сервере `{ctx.guild.name}`', description=f'Модератором {ctx.message.author.mention}', color= 0x008080)
                            embed.add_field(name='Причина:', value=f'{reason}', inline=True)
                            await user.send(embed=embed)
                        
                            embed1=discord.Embed(title= 'Успешное выполнение команды:' , description=f'Пользователю {user.mention} было выдано `1` предупреждение', color=0x008080)
                            embed1.add_field(name='Задачу выполнил:', value=f'{ctx.message.author.mention}', inline=True)
                            embed1.add_field(name='Причина:', value=f'{reason}', inline=True)
                            embed1.add_field(name='Количество:', value=f"3/3")
                            await ctx.send(embed=embed1)   

                            try:
                                cursor.execute(f"update rayabot.users set ban = 1 and warn = 0 where user_id = '{user.id}' and guild_name = '{ctx.guild.name}' ")
                                connect.commit()
                            except Exception as ex:
                                print(ex)

                            await user.ban(reason='3/3 предупреждений')

                            time = 2592000
                            await asyncio.sleep(time)
                            cursor.execute(f"update rayabot.users set ban = 0 where user_id = '{user.id}' and guild_name = '{ctx.guild.name}' ")
                            connect.commit()
                            await ctx.guild.unban(user)
                            
                    if count == 2:
                        if warns == 0:
                            cursor.execute(f"update rayabot.users set warn = warn + 2 where user_id = '{user.id}' and guild = '{ctx.guild.id}'")
                            connect.commit()
                            embed=discord.Embed(title=f'Вам выдали `2` предупреждения на сервере `{ctx.guild.name}`', description=f'Модератором {ctx.message.author.mention}', color= 0x008080)
                            embed.add_field(name='Причина:', value=f'{reason}', inline=True)
                            await user.send(embed=embed)
                        
                            embed1=discord.Embed(title= 'Успешное выполнение команды:' , description=f'Пользователю {user.mention} было выдано `2` предупреждения', color=0x008080)
                            embed1.add_field(name='Задачу выполнил:', value=f'{ctx.message.author.mention}', inline=True)
                            embed1.add_field(name='Причина:', value=f'{reason}', inline=True)
                            embed1.add_field(name='Количество:', value=f"2/3")
                            await ctx.send(embed=embed1)   




                        if warns == 1:
                            embed=discord.Embed(title=f'Вам выдали `2` предупреждения на сервере `{ctx.guild.name}`', description=f'Модератором {ctx.message.author.mention}', color= 0x008080)
                            embed.add_field(name='Причина:', value=f'{reason}', inline=True)
                            await user.send(embed=embed)
                        
                            embed1=discord.Embed(title= 'Успешное выполнение команды:' , description=f'Пользователю {user.mention} было выдано `2` предупреждения', color=0x008080)
                            embed1.add_field(name='Задачу выполнил:', value=f'{ctx.message.author.mention}', inline=True)
                            embed1.add_field(name='Причина:', value=f'{reason}', inline=True)
                            embed1.add_field(name='Количество:', value=f"3/3")
                            await ctx.send(embed=embed1)

                            try:
                                cursor.execute(f"update rayabot.users set ban = 1 and warn = 0 where user_id = '{user.id}' and guild_name = '{ctx.guild.name}' ")
                                connect.commit()
                            except Exception as ex:
                                print(ex)

                            await user.ban(reason='3/3')

                            time = 2592000
                            await asyncio.sleep(time)
                            cursor.execute(f"update rayabot.users set ban = 0 where user_id = '{user.id}' and guild_name = '{ctx.guild.name}' ")
                            connect.commit()
                            await ctx.guild.unban(user)
                            




                        if warns == 2:
                            emb3 = discord.Embed(title= "Ошибка", description = "▹ Значение должно быть равно `1` так-как максимальное количество предупреждений `3`", color=0x008080)
                            await ctx.reply(embed=emb3)



                    if count == 3:
                        if warns == 0: 
                            embed=discord.Embed(title=f'Вам выдали `3` предупреждения на сервере `{ctx.guild.name}`', description=f'Модератором {ctx.message.author.mention}', color= 0x008080)
                            embed.add_field(name='Причина:', value=f'{reason}', inline=True)
                            await user.send(embed=embed)
                        
                            embed1=discord.Embed(title= 'Успешное выполнение команды:' , description=f'Пользователю {user.mention} было выдано `3` предупреждения', color=0x008080)
                            embed1.add_field(name='Задачу выполнил:', value=f'{ctx.message.author.mention}', inline=True)
                            embed1.add_field(name='Причина:', value=f'{reason}', inline=True)
                            embed1.add_field(name='Количество:', value=f"3/3")
                            await ctx.send(embed=embed1)


                            try:
                                cursor.execute(f"update rayabot.users set ban = 1 and warn = 0 where user_id = '{user.id}' and guild_name = '{ctx.guild.name}' ")
                                connect.commit()
                            except Exception as ex:
                                print(ex)

                            await user.ban(reason='3/3')

                            time = 2592000
                            await asyncio.sleep(time)
                            cursor.execute(f"update rayabot.users set ban = 0 where user_id = '{user.id}' and guild_name = '{ctx.guild.name}' ")
                            connect.commit()
                            await ctx.guild.unban(user)
                             




                        if warns == 1:
                            emb3 = discord.Embed(title= "Ошибка", description = "▹ Значение должно быть равно `2` так-как максимальное количество предупреждений `3`", color=0x008080)
                            await ctx.reply(embed=emb3)




                        if warns == 2:
                            emb3 = discord.Embed(title= "Ошибка", description = "▹ Значение должно быть равно `1` так-как максимальное количество предупреждений `3`", color=0x008080)
                            await ctx.reply(embed=emb3)

                        if warns == 3:
                            emb3 = discord.Embed(title= "Ошибка", description = "▹ Значение должно быть равно `0` так-как максимальное количество предупреждений `3`", color=0x008080)
                            await ctx.reply(embed=emb3)

            
@warn.error
async def warn_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed=discord.Embed(title= '' , description=f'{ctx.message.author.mention} Кажеться у вас не достаточно прав.😟', color=0x008080)
        await ctx.reply(embed=embed)
    if isinstance(error, commands.MissingRequiredArgument):
        emb3 = discord.Embed(title= "Выдать предупреждение на сервере", descriptions = "▹ Выдавайте предупреждения участникам за их нарушения", color=0x008080)
        emb3.add_field(name = " Использование ", value = "▹`.warn  @<учасник> <количество> <причина>`\n ┗ `<учасник>` - может принимать цифровой ID учасника или упоминание его.\n Обезательный параметр\n ┗ `<причина>` - Необезательный параметр  " ,inline=False )
        await ctx.reply(embed=emb3)






@bot.command()
async def unwarn(ctx, user: discord.Member, count: int):
    cursor.execute(f"select * from rayabot.users where guild = '{ctx.guild.id}' and user_id = '{ctx.message.author.id}'")
    _admin = cursor.fetchone()['admin']
    cursor.execute(f"select * from rayabot.users where guild = '{ctx.guild.id}' and user_id = '{user.id}'")
    admins = cursor.fetchone()['admin']
    if _admin <4:
        emb4 = discord.Embed(title=" Что-то пошло не так ",  description= f'\n▹ Упс, у вас не недостаточно прав ', color=0xff9900)
        emb4.set_footer(text=f'Отправлено: {ctx.author}  | Тест бот (c) 2022 •   ', icon_url=ctx.author.avatar_url,  )
        message = await ctx.send(embed = emb4)
    else:
        if _admin < admins:
            embed=discord.Embed(title=f'Что-то пошло не так', description=f'Вы не можете взаемодействовать с пользователем у которого уровень администратора выше вашего! ', color= 0xffff00)
            await ctx.send(embed=embed)
        else:
            if count >= 0 and count <= 3:
                cursor.execute(f"update rayabot.users set warn = {count} where user_name = '{user}' and guild_name = '{ctx.guild.name}'")
                connect.commit()
                    
                embed=discord.Embed(title=f'Вам зняли попередження на сервері `{ctx.guild.name}`', description=f'Товаришом {ctx.message.author.mention}', color= 0x008080)
                await user.send(embed=embed)
                        
                embed1=discord.Embed(title= 'Успішне виконання завдання:' , description=f'Товаришу {user.mention} було знято попередження', color=0x008080)
                embed1.add_field(name='Задачу виконав:', value=f'{ctx.message.author.mention}', inline=True)
                await ctx.send(embed=embed1)  



@bot.command()
async def warns(ctx, user: discord.Member):
    try:
        cursor.execute(f"select * from rayabot.users where guild = '{ctx.guild.id}' and user_id = '{user.id}'")
        warn_user = cursor.fetchone()['warn']
        if warn_user == 0:
            emb4 = discord.Embed(title=f" Информация о предупреждениях пользователя {user.name}\n ",  description= f'Предупреждения отсутствуют', color=0xff9900)
            emb4.set_footer(text=f'Отправлено: {ctx.author}  | Тест бот (c) 2022 •   ', icon_url=ctx.author.avatar_url,  )
            message = await ctx.send(embed = emb4)
        if warn_user == 1:
            emb4 = discord.Embed(title=f" Информация о предупреждениях пользователя {user.name} ",  description= f'', color=0xff9900)
            emb4.add_field(name = "Количество:", value = "`1 предупреждение`")
            emb4.set_footer(text=f'Отправлено: {ctx.author}  | Тест бот (c) 2022 •   ', icon_url=ctx.author.avatar_url,  )
            message = await ctx.send(embed = emb4)
        if warn_user == 2:
            emb4 = discord.Embed(title=f" Информация о предупреждениях пользователя {user.name} ",  description= f'', color=0xff9900)
            emb4.add_field(name = "Количество:", value = "`2 предупреждения`")
            emb4.set_footer(text=f'Отправлено: {ctx.author}  | Тест бот (c) 2022 •   ', icon_url=ctx.author.avatar_url,  )
            message = await ctx.send(embed = emb4)
    except Exception as ex:
        print(ex)


@warns.error
async def warns(ctx, error):
    cursor.execute(f"select * from rayabot.users where guild = '{ctx.guild.id}' and user_id = '{ctx.message.author.id}'")
    warn_message = cursor.fetchone()['warn']
    if isinstance(error, commands.MissingRequiredArgument):
        if warn_message == 0:
            emb4 = discord.Embed(title=f" Информация о предупреждениях пользователя {ctx.message.author.name}\n ",  description= f'Предупреждения отсутствуют', color=0xff9900)
            emb4.set_footer(text=f'Отправлено: {ctx.author}  | Райя бот (c) 2022 •   ', icon_url=ctx.author.avatar_url,  )
            message = await ctx.send(embed = emb4)
        if warn_message == 1:
            emb4 = discord.Embed(title=f" Информация о предупреждениях пользователя {ctx.message.author.name} ",  description= f'', color=0xff9900)
            emb4.add_field(name = "Количество:", value = "`1 предупреждение`")
            emb4.set_footer(text=f'Отправлено: {ctx.author}  | Райя бот (c) 2022 •   ', icon_url=ctx.author.avatar_url,  )
            message = await ctx.send(embed = emb4)
        if warn_message == 2:
            emb4 = discord.Embed(title=f" Информация о предупреждениях пользователя {ctx.message.author.name} ",  description= f'', color=0xff9900)
            emb4.add_field(name = "Количество:", value = "`2 предупреждения`")
            emb4.set_footer(text=f'Отправлено: {ctx.author}  | Райя бот (c) 2022 •   ', icon_url=ctx.author.avatar_url,  )
            message = await ctx.send(embed = emb4)


# @bot.command()
# async def admins(ctx):
#     cursor.execute(f"select * from rayabot.users where guild = '{ctx.guild.id}' and user_id = '{user.id}'")
#     _admin = cursor.fetchall()['admin']
#     emb4 = discord.Embed(title=f"Список администрации",  description= f'', color=0xff9900)
#     emb4.add_field(name = "Создатель:", value = f"{ctx.guild.owner.name}")
#     emb4.add_field(name = "5 уровень администратора", value = f"{_admin}" ,inline= False)
#     emb4.add_field(name = "4 уровень администратора", value = f"4",inline= False)
#     emb4.add_field(name = "3 уровень администратора", value = f"3",inline= False)
#     emb4.add_field(name = "2 уровень администратора", value = f"2",inline= False)
#     emb4.add_field(name = "1 уровень администратора", value = f"1",inline= False)
#     emb4.set_footer(text=f'Отправлено: {ctx.author}  | Райя Бот (c) 2022 •   ', icon_url=ctx.author.avatar_url,  )
#     message = await ctx.send(embed = emb4)



#-----------------------------------------------------------happy-------------------------------------------------------------------------------------
@bot.command()
async def dog(ctx):
    response = requests.get('https://some-random-api.ml/img/dog') # Get-запрос
    json_data = json.loads(response.text) # Извлекаем JSON

    embed = discord.Embed(color = 0x008080) # Создание Embed'a
    embed.set_image(url = json_data['link']) # Устанавливаем картинку Embed'a
    await ctx.send(embed = embed) # Отправляем Embed

@bot.command()
async def cat(ctx):
    response = requests.get('https://some-random-api.ml/img/cat') # Get-запрос
    json_data = json.loads(response.text) # Извлекаем JSON

    embed = discord.Embed(color = 0x008080) # Создание Embed'a
    embed.set_image(url = json_data['link']) # Устанавливаем картинку Embed'a
    await ctx.send(embed = embed) # Отправляем Embed

@bot.command()
async def panda(ctx):
    response = requests.get('https://some-random-api.ml/img/panda') # Get-запрос
    json_data = json.loads(response.text) # Извлекаем JSON

    embed = discord.Embed(color = 0x008080) # Создание Embed'a
    embed.set_image(url = json_data['link']) # Устанавливаем картинку Embed'a
    await ctx.send(embed = embed) # Отправляем Embed

@bot.command(aliases=['COIN'])
async def coin(ctx,* , count):

        coin = [
              "Орёл",
              "Решка"            
        ]
        if count == "Орёл" or count == "орел":
            emb1 = discord.Embed(title="",  description= f'`Орёл говоришь?` Хмм... Щас посмотрим, мне кажеться тебе выпало: `{random.choice(coin)}` ', color=0x008080)
            message = await ctx.send(embed = emb1)
        if count == "Решка":
            emb1 = discord.Embed(title="",  description= f'`Решка` говоришь? Хмм... Щас посмотрим мне кажеться тебе выпало: `{random.choice(coin)}` ', color=0x008080)
            message = await ctx.send(embed = emb1)


@bot.command(aliases=['BALL'])
async def ball(ctx, *, count):
        ball = [
              "Сейчас не могу предсказать :eyes:",
              "Мой ответ — нет :broken_heart:",
              "Даже не думай :x:",
              "Знаки говорят — да :ok_hand:",
              "По моим данным — нет :no_entry_sign:",
              "Весьма сомнительно :question:",
              "Мне кажется — да :ok_hand::",
              "Перспективы не очень хорошие :no_entry:",
              "Предрешено :thumbsup:", 
              "Да :ok_hand:"          
        ]
        emb4 = discord.Embed(title="*Вопрос:*",  description= f'▹ {count} ', color=0x008080)
        emb4.add_field(name = " *Ответ:*  ", value = f"▹ {random.choice(ball)} ")
        message = await ctx.send(embed = emb4)










#---------------------------------------------------info------------------------------------------------------------------------------------------------------------

@bot.command()
async def raya(ctx):
    count = 0
    membercount = 0
    ping = str(bot.latency * 60)
    channels_count = 0
    for guild in bot.guilds:
        count += 1
    
    for guild in bot.guilds:
        for member in guild.members:    
            membercount += 1

    for guild in bot.guilds:
        channels_count += len(guild.channels)

    try:
        emb2 = discord.Embed(title="Статистика Raya Bot", color=0x008080)
        emb2.add_field(name = "**Основная**", value=f'**Серверов: {count} ** \n **Пользователей: {membercount} ** \n **Каналов:{channels_count}** \n' )
        emb2.add_field(name = "Платформа", value=f'**Библиотека: DISCORD.PY (v3.8.9) ** \n **Версия бота: 0.2** \n **Пинг бота: {ping[:1]}ms **\n **Запущен:** \n' )
        message = await ctx.send(embed=emb2)
    except Exception as ex:
        print(ex)



@bot.command(aliases = ['SERVER'])
async def server(ctx):       
    embed = discord.Embed(
        description = f'Информация о сервере **{ctx.guild.name}**\n'
                      f'\n'
                      f'**Участники:**\n'
                      f'▹ Людей: **{ctx.guild.member_count}**\n'
                      f'\n'
                      f'**Каналы:**\n'
                      f'▹ Текстовые: **{len(ctx.guild.text_channels)}**\n'
                      f'▹ Голосовые: **{len(ctx.guild.voice_channels)}**\n'
                      f'▹ Категории: **{len(ctx.guild.categories)}**\n'
                      f'\n'
                      f'**Владелец:**\n'
                      f'▹ {ctx.guild.owner}\n'
                      f'\n'
                      f'**Уровень проверки:**\n'
                      f'▹ {ctx.guild.verification_level}\n'
                      f'\n'
                      f'**Дата создания:**\n▹ {ctx.guild.created_at.strftime("%d.%m.%Y")}\n',
                     color=0x008080,)
    embed.set_footer(text = f'ID: {ctx.guild.id}')
    embed.set_thumbnail(url = str(ctx.guild.icon_url))
    await ctx.send(embed=embed)


@bot.command()
async def slowmode(ctx, count):
    cursor.execute(f"select * from rayabot.users where guild = '{ctx.guild.id}' and user_id = '{ctx.message.author.id}'")
    _admin = cursor.fetchone()['admin']
    if _admin <5:
        emb4 = discord.Embed(title=" Что-то пошло не так ",  description= f'\n▹ Упс, у вас не недостаточно прав ', color=0xff9900)
        emb4.set_footer(text=f'Отправлено: {ctx.author}  | Тест бот (c) 2022 •   ', icon_url=ctx.author.avatar_url,  )
        message = await ctx.send(embed = emb4)
    else:
        await ctx.channel.edit(slowmode_delay=count)
        emb4 = discord.Embed(title="Успешно :white_check_mark: ",  description= f'Вы установили задержку чата в {count} секунд', color=0x008080)
        message = await ctx.send(embed = emb4)
        if count == 0:
            await ctx.channel.edit(slowmode_delay=0)
            emb4 = discord.Embed(title="Успешно :white_check_mark: ",  description= f'Вы удалили задержку чата', color=0x008080)
            message = await ctx.send(embed = emb4)


#--------------------------------------------.clear--------------------------------------------------------------------------------------------------
@bot.command()
async def clear(ctx, amount):
    cursor.execute(f"select * from rayabot.users where guild = '{ctx.guild.id}' and user_id = '{ctx.message.author.id}'")
    _admin = cursor.fetchone()['admin']
    if _admin <2:
        emb4 = discord.Embed(title=" Что-то пошло не так ",  description= f'\n▹ Упс, у вас не недостаточно прав ', color=0xff9900)
        emb4.set_footer(text=f'Отправлено: {ctx.author}  | Тест бот (c) 2022 •   ', icon_url=ctx.author.avatar_url,  )
        message = await ctx.send(embed = emb4)
    else:
        await ctx.channel.purge(limit=int(amount))
        emb4 = discord.Embed(title="Успешно :white_check_mark: ",  description= f'Cообщений было очищено: {amount}', color=0x008080)
        message = await ctx.send(embed = emb4)


@clear.error
async def сlear(ctx, error):
    try: 
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title= 'Ошибка :x: ' , description=f'{ctx.message.author.mention} Вы не можете использовать данную команду, вам не хватает прав!', color=0x008080)
            await ctx.reply(embed=embed)
        if isinstance(error, commands.MissingRequiredArgument):
            emb3 = discord.Embed(title="Очистить последние сообщения в текущем канале", color=0x008080)
            emb3.add_field(name = " Использование ", value = "`.clear <количество сообщений>`\n ┗ Параметр <> обезательное к использованию. " ,inline=False )
            emb3.add_field(name = " Пример ", value = "`.clear 10`\n ┗ Удалит последние 10 сообщений в текущем канале. " ,inline=False )
            emb3.add_field(name = " Важно ", value = "`При удалении большого количества сообщений нужно больше подождать до момента пока вы не получите сообщение от бота что все сообщения удалены`\n ┗ Проблема в лимитах Discord'а  " ,inline=False )
            await ctx.reply(embed=emb3)
    except Exception as ex:
        print(ex)
#----------------------------------------.kick------------------------------------------------------------------------------------------------------------

@bot.command()
async def kick(ctx, user: discord.Member, *, reason = None):
    cursor.execute(f"select * from rayabot.users where guild = '{ctx.guild.id}' and user_id = '{ctx.message.author.id}'")
    _admin = cursor.fetchone()['admin']
    cursor.execute(f"select * from rayabot.users where guild = '{ctx.guild.id}' and user_id = '{user.id}'")
    admins = cursor.fetchone()['admin']
    if _admin <3:
        emb4 = discord.Embed(title=" Что-то пошло не так ",  description= f'\n▹ Упс, у вас не недостаточно прав ', color=0xff9900)
        emb4.set_footer(text=f'Отправлено: {ctx.author}  | Тест бот (c) 2022 •   ', icon_url=ctx.author.avatar_url,  )
        message = await ctx.send(embed = emb4)
    else:
        if _admin < admins:
            embed=discord.Embed(title=f'Что-то пошло не так', description=f'Вы не можете взаемодействовать с пользователем у которого уровень администратора выше вашего! ', color= 0xffff00)
            await ctx.send(embed=embed)
        else:
          if not reason:
            await user.kick()
            emb4 = discord.Embed(title="Успешное выполнение команды :white_check_mark: ",  description= f'▹Учасник {user.mention} исключен\n ', color=0x008080)
            emb4.add_field(name = " Команду выполнил \n ", value = f"▹ {ctx.message.author.mention}")
            message = await ctx.send(embed = emb4)
          else:
            await user.kick(reason=reason)
            emb4 = discord.Embed(title="Успешное выполнение команды :white_check_mark: ",  description= f'▹Учасник {user.mention} исключен\n ', color=0x008080)
            emb4.add_field(name = " Команду выполнил \n ", value = f"▹ {ctx.message.author.mention}")
            emb4.add_field(name = " Причиной тому стало \n ", value =  f"▹ {reason}")
            message = await ctx.send(embed = emb4)


@kick.error
async def kick(ctx, error):
    try: 
        if isinstance(error, commands.MissingPermissions):
            embed=discord.Embed(title= 'Ошибка доступа :x:' , description=f'{ctx.message.author.mention} Вы не можете использовать данную команду, вам не хватает прав!', color=0x008080)
            await ctx.reply(embed=embed)
        if isinstance(error, commands.MissingRequiredArgument):
            emb3 = discord.Embed(title= "Исключить из сервера", descriptions = "▹ У вас есть возможность изгнать учасника, но при этом у него останеться возможность вернуться обратно.",color=0x008080)
            emb3.add_field(name = " Использование ", value = "▹`.kick  @<учасник> <причина>`\n ┗ `<учасник>` - может принимать цифровой ID учасника или упоминание его.\n Обезательный параметр\n ┗ `<причина>` - Необезательный параметр  " ,inline=False )
            await ctx.reply(embed=emb3)
    except Exception as ex:
        print(ex)

#------------------------------------------------------------------------------.mute----------------------------------------------------------
@bot.command(pass_context = True, aliases=["Mute", "MUte", "MUTe", "MUTE", "mutE", "muTE", "mUTE", "MuTe", "mUtE"])
async def mute(ctx, user: discord.Member,  time: int = None,*, reason=None):
    cursor.execute(f"select * from rayabot.users where guild = '{ctx.guild.id}' and user_id = '{ctx.message.author.id}'")
    _admin = cursor.fetchone()['admin']
    cursor.execute(f"select * from rayabot.users where guild = '{ctx.guild.id}' and user_id = '{user.id}'")
    admins = cursor.fetchone()['admin']
    if _admin <3:
        emb4 = discord.Embed(title=" Что-то пошло не так ",  description= f'\n▹ Упс, у вас не недостаточно прав ', color=0xff9900)
        emb4.set_footer(text=f'Отправлено: {ctx.author}  | Тест бот (c) 2022 •   ', icon_url=ctx.author.avatar_url,  )
        message = await ctx.send(embed = emb4)
    else:
        if _admin < admins:
            embed=discord.Embed(title=f'Что-то пошло не так', description=f'Вы не можете взаемодействовать с пользователем у которого уровень администратора выше вашего! ', color= 0xffff00)
            await ctx.send(embed=embed)
        else:
            role = discord.utils.get(ctx.guild.roles, name='Mute by Raya') #роль мута
            if role in user.roles:
                emb4 = discord.Embed(title=" Что-то пошло не так ",  description= f'\n▹ Упс, учасник уже заблокирован в данных каналах ', color=0x008080)
                emb4.set_footer(text=f'Отправлено: {ctx.author}  | Тест бот (c) 2022 •   ', icon_url=ctx.author.avatar_url,  )
                message = await ctx.send(embed = emb4) 
            elif time >=1441:
                emb4 = discord.Embed(title=" Что-то пошло не так ",  description= f'\n▹ Время должно быть больше/равно 1 и меньше/равно 1440 ', color=0x008080)
                emb4.set_footer(text=f'Отправлено: {ctx.author}  | Тест бот (c) 2022 •   ', icon_url=ctx.author.avatar_url,  )
                message = await ctx.send(embed = emb4)
            elif time <1:
                emb4 = discord.Embed(title=" Что-то пошло не так ",  description= f'\n▹ Время должно быть больше/равно 1 и меньше/равно 1440 ', color=0x008080)
                emb4.set_footer(text=f'Отправлено: {ctx.author}  | Тест бот (c) 2022 •   ', icon_url=ctx.author.avatar_url,  )
                message = await ctx.send(embed = emb4)
            else:
                if not reason:
                    emb4 = discord.Embed(title=f"Успешное выполнение команды", description = f"▹Учасник {user.mention} получил блокировку в текстовых каналах", color=0x008080) 
                    emb4.add_field(name = "Команду выполнил", value = f"\n ▹ {ctx.message.author.mention} "  )
                    emb4.add_field(name = "Время", value = f"\n {time} мин. "  )
                    await ctx.send(embed=emb4)
                else:
                    emb4 = discord.Embed(title=f"Успешное выполнение команды", description = f"▹Учасник {user.mention} получил блокировку в текстовых каналах", color=0x008080) 
                    emb4.add_field(name = "Команду выполнил", value = f"\n ▹ {ctx.message.author.mention} "  )
                    emb4.add_field(name = "Время", value = f"\n {time} мин. "  )
                    emb4.add_field(name = "Причиной тому стало", value = f"\n ▹ {reason}", inline = False) 
                    await ctx.send(embed=emb4)
                await user.add_roles(role) #видает роль
                guild = ctx.guild
                for channels in guild.channels:
                    await channels.set_permissions(role, send_messages=False)
                time = time * 60
                await asyncio.sleep(time)
                await user.remove_roles(role)

@mute.error
async def mute(ctx, error):
    try: 
        if isinstance(error, commands.MissingRequiredArgument):
            emb3 = discord.Embed(title= "Бан в текстовых каналах", description = "▹ Участник нарушает правила текстового канала? Накажите его блокировкой чата. Вы можете выдать мут от 1 минуты и до 24-ех часов", color=0x008080)
            emb3.add_field(name = " Используйте ", value = "▹`.mute  @<учасник> <время> <причина>`\n ┗ `<участник>` - может принимать цифровой ID участника или упоминание его. Обязательный параметр\n ┗ `<время>` - принимает только числа от 1 и до 1440 (24 часа). Обязательный параметр \n ┗ `<причина>` - Необязательный параметр" ,inline=False )
            await ctx.reply(embed=emb3)
    except Exception as ex:
        print(ex)

#----------------------------------------------------unmute-----------------------------------------------------------------------------
@bot.command()
async def unmute(ctx, user: discord.Member):
    cursor.execute(f"select * from rayabot.users where guild = '{ctx.guild.id}' and user_id = '{ctx.message.author.id}'")
    _admin = cursor.fetchone()['admin']
    cursor.execute(f"select * from rayabot.users where guild = '{ctx.guild.id}' and user_id = '{user.id}'")
    admins = cursor.fetchone()['admin']
    if _admin <3:
        emb4 = discord.Embed(title=" Что-то пошло не так ",  description= f'\n▹ Упс, у вас не недостаточно прав ', color=0xff9900)
        emb4.set_footer(text=f'Отправлено: {ctx.author}  | Тест бот (c) 2022 •   ', icon_url=ctx.author.avatar_url,  )
        message = await ctx.send(embed = emb4)
    else:
        if _admin < admins:
            embed=discord.Embed(title=f'Что-то пошло не так', description=f'Вы не можете взаемодействовать с пользователем у которого уровень администратора выше вашего! ', color= 0xffff00)
            await ctx.send(embed=embed)
        else:
            try: 
                mutedRole = discord.utils.get(ctx.guild.roles, name="Mute by Raya")
                author = ctx.message.author
                if user == author:
                    emb4 = discord.Embed(title=" Что-то пошло не так ",  description= f'\n▹ Упс, вы не можете розмутить самого себя ', color=0x008080)
                    emb4.set_footer(text=f'Отправлено: {ctx.author}  | Тест бот (c) 2022 •   ', icon_url=ctx.author.avatar_url,  )
                    message = await ctx.send(embed = emb4)
                elif mutedRole not in user.roles:
                        emb4 = discord.Embed(title=" Что-то пошло не так ",  description= f'\n▹ Упс, кажеться пользователь не замучен ', color=0x008080)
                        emb4.set_footer(text=f'Отправлено: {ctx.author}  | Тест бот (c) 2022 •   ', icon_url=ctx.author.avatar_url,  )
                        message = await ctx.send(embed = emb4)
                else:
                    await user.remove_roles(mutedRole)
                    emb4 = discord.Embed(title=f"Амнистия", description = f"▹ Учасник {user.mention} разблокирован в текстовых каналах администратором", color = 0x008080) 
                    emb4.add_field(name = "Пожалел", value = f"\n ▹ {ctx.message.author.mention} "  )
                    await ctx.send(embed=emb4)
            except Exception as ex:
                print(ex)

@unmute.error
async def unmute_error(ctx, error):
        if isinstance(error, commands.BadArgument):
            emb4 = discord.Embed(title=" Что-то пошло не так ",  description= f'\n▹ Упс, кажеться пользователь не найден. ', color=0x008080)
            emb4.set_footer(text=f'Отправлено: {ctx.author}  | Тест бот (c) 2022 •   ', icon_url=ctx.author.avatar_url,  )
            message = await ctx.send(embed = emb4)





@bot.command()
async def welcome(ctx, * , text):
    cursor.execute(f"select * from rayabot.users where guild = '{ctx.guild.id}' and user_id = '{ctx.message.author.id}'")
    _admin = cursor.fetchone()['admin']
    if _admin <6:
        emb4 = discord.Embed(title=" Что-то пошло не так ",  description= f'\n▹ Упс, у вас не недостаточно прав ', color=0xff9900)
        emb4.set_footer(text=f'Отправлено: {ctx.author}  | Тест бот (c) 2022 •   ', icon_url=ctx.author.avatar_url,  )
        message = await ctx.send(embed = emb4)
    else:
        cursor.execute(f"select * from rayabot.guilds where guild_id = '{ctx.guild.id}'")
        _welcome = cursor.fetchone()['welcome']
        if text == "get":
            emb4 = discord.Embed(title=" Приветствие учасника ",  description= f'\n▹ {_welcome}  ', color=0x008080)
            message = await ctx.send(embed = emb4)
        elif text == "remove":
            cursor.execute(f"update rayabot.guilds set welcome = Null where guild_id = '{ctx.guild.id}'")
            connect.commit()
            emb4 = discord.Embed(title=" Успешно ",  description= f'\n▹ Приветствие нового участника удалено. ', color=0x008080)
            message = await ctx.send(embed = emb4)
        else:
            cursor.execute(f"update rayabot.guilds set welcome = '{text}' where guild_id = '{ctx.guild.id}'")
            connect.commit()
            emb4 = discord.Embed(title=" Успешно ",  description= f'\n▹ Приветствие нового участника было добавлено. ', color=0x008080)
            message = await ctx.send(embed = emb4)
@welcome.error
async def welcome_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed=discord.Embed(title= 'Ошибка доступа :x:' , description=f'{ctx.message.author.mention} Вы не можете использовать данную команду, вам не хватает прав!', color=0x008080)
        await ctx.reply(embed=embed)
    if isinstance(error, commands.MissingRequiredArgument):
        emb3 = discord.Embed(title= "Настройка приветствия сервера", descriptions = "▹ ▹ Устанавливайте приветствие участника, чтобы было понятно :3",color=0x008080)
        emb3.add_field(name = " Использование ", value = "▹`.welcome <тип>`\n ┗ `<текст>` - Устанавливает приветствие сервера\n ┗ `<remove>` - Удаляет приветствие сервера\n ┗ `<get>` - Узнает приветствие сервера " ,inline=False )
        emb3.add_field(name = " Пример 1 ", value = "▹`.welcome Ты няшка :З`\n ┗ Добавите приветствие сервера  " ,inline=False )
        emb3.add_field(name = " Пример 2 ", value = "▹`.welcome remove `\n ┗ Удалит приветствие сервера " ,inline=False )
        emb3.add_field(name = " Пример 3 ", value = "▹`.welcome get `\n ┗ Узнаете приветствие сервера " ,inline=False )
        await ctx.reply(embed=emb3)

















@bot.command(aliases=["допомога", "помощь"])
async def help(ctx ,amount):
    if amount == "help":
        emb1 = discord.Embed(title="Команда `.help`",  description= 'Показывает список всех доступных команд бота', color=0x008080)
        emb1.add_field(name = "Уровень администратора:", value="Не требуються", inline=False)
        message = await ctx.send(embed = emb1)

    if amount == "raya":
        emb1 = discord.Embed(title="Команда `.raya`",  description= 'Данная команда показывает статисику бота', color=0x008080)
        emb1.add_field(name = "Уровень администратора:", value="Не требуються", inline=False)
        message = await ctx.send(embed = emb1)

    if amount == "server":
        emb1 = discord.Embed(title="Команда `.server`",  description= 'Показывает статисику текущего сервера', color=0x008080)
        emb1.add_field(name = "Уровень администратора:", value="Не требуються", inline=False)
        message = await ctx.send(embed = emb1)

    if amount == "get":
        emb1 = discord.Embed(title="Команда `.get`",  description= 'Показывает информацию о пользователе', color=0x008080)
        emb1.add_field(name = "Уровень администратора:", value="1-й уровень", inline=False)
        emb1.add_field(name = " Используйте ", value = "▹`.get  @<учасник>`\n ┗ `<участник>` - может принимать цифровой ID участника или упоминание его." ,inline=False )
        message = await ctx.send(embed = emb1)

    if amount == "warn":
        emb1 = discord.Embed(title="Команда `.warn`",  description= 'С помощю данной команды вы можете выдать предупреждение пользователю', color=0x008080)
        emb1.add_field(name = "Уровень администратора:", value="4-й уровень", inline=False)
        emb1.add_field(name = " Используйте ", value = "▹.warn  `@<учасник>` `<количество>` `<причина>`\n ┗ `<участник>` - может принимать цифровой ID участника или упоминание его.\n ┗ `<количество>` - количество предупрeждений, количество не должно быть меньше 0 или больше 3х \n ┗ - `<причина>` - Необезательный параметр` " ,inline=False )
        message = await ctx.send(embed = emb1)

    if amount == "unwarn":
        emb1 = discord.Embed(title="Команда `.unwarn`",  description= 'С помощю данной команды вы можете снять предупреждение пользователю', color=0x008080)
        emb1.add_field(name = "Уровень администратора:", value="4-й уровень администратора", inline=False)
        emb1.add_field(name = " Используйте ", value = "▹.unwarn  `@<учасник>` `<количество>`\n ┗ `<участник>` - может принимать цифровой ID участника или упоминание его.\n ┗ `<количество>` - количество предупрeждений, количество не должно быть меньше 0 или больше 3х " ,inline=False )
        message = await ctx.send(embed = emb1)

    if amount == "mute":
        emb1 = discord.Embed(title="Команда `.mute`",  description= 'С помощю данной команды вы можете выдать блокировку текстового чата пользователю', color=0x008080)
        emb1.add_field(name = "Уровень администратора:", value="3-й уровень", inline=False)
        emb1.add_field(name = " Используйте ", value = "▹.mute  `@<учасник>` `<время> <причина>`\n ┗ `<участник>` - может принимать цифровой ID участника или упоминание его.\n ┗ <время> - на сколько будет выдана блокировка. Максимальное время выдачи мута 1440 минут(24ч) \n ┗ `<количество>` - количество предупрeждений, количество не должно быть меньше 0 или больше 3х " ,inline=False )
        message = await ctx.send(embed = emb1)

    if amount == "unmute":
        emb1 = discord.Embed(title="Команда `.unmute`",  description= 'С помощю данной команды вы можете снять текстовую блокировку чата пользователю', color=0x008080)
        emb1.add_field(name = "Уровень администратора:", value="3-й уровень", inline=False)
        emb1.add_field(name = " Используйте ", value = "▹.unmute  `@<учасник>`\n ┗ `<участник>` - может принимать цифровой ID участника или упоминание его. " ,inline=False )
        message = await ctx.send(embed = emb1)
    if amount == "kick":
        emb1 = discord.Embed(title="Команда `.kick`",  description= 'С помощю данной команды вы можете выгнать пользователя с сервера', color=0x008080)
        emb1.add_field(name = "Уровень администратора", value="3-й уровень", inline=False)
        emb1.add_field(name = " Используйте ", value = "▹.kick  `@<учасник>` `<причина>`\n ┗ `<участник>` - может принимать цифровой ID участника или упоминание его.\n ┗ `<причина>` - Необезательный параметр " ,inline=False )
        message = await ctx.send(embed = emb1)
    if amount == "clear":
        emb1 = discord.Embed(title="Команда `.clear`",  description= 'С помощю данной команды вы можете очистить сообщение в любом текстовом канале(до которого у вас есть доступ)', color=0x008080)
        emb1.add_field(name = "Уровень администратора:", value="2-й уровень", inline=False)
        emb1.add_field(name = " Используйте ", value = "▹.clear `<количество>`\n ┗ `<количество>` - количество удаленных сообщений " ,inline=False )
        message = await ctx.send(embed = emb1)
    if amount == "cat":
        emb1 = discord.Embed(title="Команда `.cat`",  description= 'Скинет фото рандомного кота', color=0x008080)
        emb1.add_field(name = "Права:", value="Не требуються", inline=False)
        message = await ctx.send(embed = emb1)
    if amount == "dog":
        emb1 = discord.Embed(title="Команда `.dog`",  description= 'Скинет фото рандомной собаки', color=0x008080)
        emb1.add_field(name = "Уровень администратора:", value="Не требуються", inline=False)
        message = await ctx.send(embed = emb1)
    if amount == "panda":
        emb1 = discord.Embed(title="Команда `.panda`",  description= 'Скинет фото рандомной панды', color=0x008080)
        emb1.add_field(name = "Уровень администратора:", value="Не требуються", inline=False)
        message = await ctx.send(embed = emb1)
    if amount == "coin":
        emb1 = discord.Embed(title="Команда `.coin`",  description= "Данная команда бросит монетку", color=0x008080)
        emb1.add_field(name = "Уровень администратора:", value="Не требуються", inline=False)
        emb1.add_field(name = " Используйте ", value = "▹.coin `<Орёл/Решка>` " ,inline=False )
        message = await ctx.send(embed = emb1)
    if amount == "ball":
        emb1 = discord.Embed(title="Команда `.ball`",  description= "Данная команда бросит шар предсказаний", color=0x008080)
        emb1.add_field(name = "Уровень администратора:", value="Не требуються", inline=False)
        emb1.add_field(name = " Используйте ", value = "▹.ball `<любой ваш вопрос>` " ,inline=False )
        message = await ctx.send(embed = emb1)
    if amount == "welcome":
        emb1 = discord.Embed(title="Команда `.welcome`",  description= "Данной командой вы можете настроить приветсвие учасников на сервере", color=0x008080)
        emb1.add_field(name = "Уровень администратора:", value="6-й уровень", inline=False)
        emb1.add_field(name = " Использование ", value = "▹`.welcome <тип>`\n ┗ `<текст>` - Устанавливает приветствие сервера\n ┗ `<remove>` - Удаляет приветствие сервера\n ┗ `<get>` - Узнает приветствие сервера " ,inline=False )
        emb1.add_field(name = " Пример 1 ", value = "▹`.welcome Ты няшка :З`\n ┗ Добавите приветствие сервера  " ,inline=False )
        emb1.add_field(name = " Пример 2 ", value = "▹`.welcome remove `\n ┗ Удалит приветствие сервера " ,inline=False )
        emb1.add_field(name = " Пример 3 ", value = "▹`.welcome get `\n ┗ Узнаете приветствие сервера " ,inline=False )
        message = await ctx.send(embed = emb1)

        






@help.error
async def help_error(ctx, error):
    cursor.execute(f"select * from rayabot.users where guild = '{ctx.guild.id}' and user_id = '{ctx.message.author.id}'")
    _admin = cursor.fetchone()['admin']
    if isinstance(error, commands.MissingRequiredArgument):
        if _admin == 0:
            emb1 = discord.Embed(title=":rosette: Список доступных команд",  description= 'В данном списке, вы можете ознакомиться с командами бота', color=0x008080)
            emb1.add_field(name = "📋  Информация (!help Information)", value="`.help` `.raya` `.server`", inline=False)
            emb1.add_field(name = "😄  Весёлое (!help Fun)", value="`.cat` `.dog` `.panda` `.coin` `.ball`", inline=False)
            emb1.set_footer(text=f'Команды обычного пользователя | RayaBot (c) 2022 •  ')
            message = await ctx.send(embed = emb1)

        if _admin == 1:
            emb1 = discord.Embed(title=":rosette: Список доступных команд",  description= 'В данном списке, вы можете ознакомиться с командами бота', color=0x008080)
            emb1.add_field(name = "📋  Информация (!help Information)", value="`.help` `.raya` `.server` `.get`", inline=False)
            emb1.add_field(name = "😄  Весёлое (!help Fun)", value="`.cat` `.dog` `.panda` `.coin` `.ball`", inline=False)
            emb1.set_footer(text=f'Команды 1-го уровня администратора | RayaBot (c) 2022 •  ')
            message = await ctx.send(embed = emb1)

        if _admin == 2:
            emb1 = discord.Embed(title=":rosette: Список доступных команд",  description= 'В данном списке, вы можете ознакомиться с командами бота', color=0x008080)
            emb1.add_field(name = "📋  Информация (!help Information)", value="`.help` `.raya` `.server` `.get`", inline=False)
            emb1.add_field(name = "🛡️  Модерирование (!help Moderation)", value="`.clear`", inline=False)
            emb1.add_field(name = "😄  Весёлое (!help Fun)", value="`.cat` `.dog` `.panda` `.coin` `.ball`", inline=False)
            emb1.set_footer(text=f'Команды 2-го уровня администратора | RayaBot (c) 2022 •  ')
            message = await ctx.send(embed = emb1)
        if _admin == 3:
            emb1 = discord.Embed(title=":rosette: Список доступных команд",  description= 'В данном списке, вы можете ознакомиться с командами бота', color=0x008080)
            emb1.add_field(name = "📋  Информация (!help Information)", value="`.help` `.raya` `.server` `.get`", inline=False)
            emb1.add_field(name = "🛡️  Модерирование (!help Moderation)", value="`.clear` `.mute` `.unmute` `.kick`", inline=False)
            emb1.add_field(name = "😄 Весёлое (!help Fun)", value="`.cat` `.dog` `.panda` `.coin` `.ball`", inline=False)
            emb1.set_footer(text=f'Команды 3-го уровня администратора | RayaBot (c) 2022 •  ')
            message = await ctx.send(embed = emb1)

        if _admin == 4:
            emb1 = discord.Embed(title=":rosette: Список доступных команд",  description= 'В данном списке, вы можете ознакомиться с командами бота', color=0x008080)
            emb1.add_field(name = "📋  Информация (!help Information)", value="`.help` `.raya` `.server` `.get`", inline=False)
            emb1.add_field(name = "🛡️  Модерирование (!help Moderation)", value="`.clear` `.mute` `.unmute` `.kick` `.warn` `unwarn` `.ban` `.unban`", inline=False)
            emb1.add_field(name = "😄 Весёлое (!help Fun)", value="`.cat` `.dog` `.panda` `.coin` `.ball`", inline=False)
            emb1.set_footer(text=f'Команды 4-го уровня администратора | RayaBot (c) 2022 •  ')
            message = await ctx.send(embed = emb1)

        if _admin == 5:
            emb1 = discord.Embed(title=":rosette: Список доступных команд",  description= 'В данном списке, вы можете ознакомиться с командами бота', color=0x008080)
            emb1.add_field(name = "📋  Информация (!help Information)", value="`.help` `.raya` `.server` `.get`", inline=False)
            emb1.add_field(name = "🛡️  Модерирование (!help Moderation)", value="`.clear` `.mute` `.unmute` `.kick` `.warn` `unwarn` `.ban` `.unban` `.setadm`", inline=False)
            emb1.add_field(name = "😄 Весёлое (!help Fun)", value="`.cat` `.dog` `.panda` `.coin` `.ball`", inline=False)
            emb1.set_footer(text=f'Команды 5-го уровня администратора | RayaBot (c) 2022 •  ')
            message = await ctx.send(embed = emb1)

        if _admin == 6:
            emb1 = discord.Embed(title=":rosette: Список доступных команд",  description= 'В данном списке, вы можете ознакомиться с командами бота', color=0x008080)
            emb1.add_field(name = "📋  Информация (!help Information)", value="`.help` `.raya` `.server` `.get` `.welcome`", inline=False)
            emb1.add_field(name = "🛡️  Модерирование (!help Moderation)", value="`.clear` `.mute` `.unmute` `.kick` `.warn` `unwarn` `.ban` `.unban` `.setadm`", inline=False)
            emb1.add_field(name = "😄 Весёлое (!help Fun)", value="`.cat` `.dog` `.panda` `.coin` `.ball`", inline=False)
            emb1.set_footer(text=f'Команды основателя сервера | RayaBot (c) 2022 •  ')
            message = await ctx.send(embed = emb1)











@bot.command()
async def setadm(ctx, user: discord.Member,*, count: int):
    try:
        cursor.execute(f"select * from rayabot.users where guild = '{ctx.guild.id}' and user_id = '{ctx.message.author.id}'")
        _admin = cursor.fetchone()['admin']
        cursor.execute(f"select * from rayabot.users where guild = '{ctx.guild.id}' and user_id = '{user.id}'")
        admins = cursor.fetchone()['admin']
        if _admin <5:
            emb4 = discord.Embed(title=" Что-то пошло не так ",  description= f'\n▹ Упс, у вас не недостаточно прав ', color=0xff9900)
            emb4.set_footer(text=f'Отправлено: {ctx.author}  | Тест бот (c) 2022 •   ', icon_url=ctx.author.avatar_url,  )
            message = await ctx.send(embed = emb4)
        else:
            if _admin < admins:
                embed=discord.Embed(title=f'Что-то пошло не так', description=f'Вы не можете взаемодействовать с пользователем у которого уровень администратора выше вашего! ', color= 0xffff00)
                await ctx.send(embed=embed)
            else:
                if user == ctx.message.author:
                    emb4 = discord.Embed(title=" Что-то пошло не так ",  description= f'\n▹ Упс, вы не можете повысить самого себя ', color=0xff9900)
                    emb4.set_footer(text=f'Отправлено: {ctx.author}  | Тест бот (c) 2022 •   ', icon_url=ctx.author.avatar_url,  )
                    message = await ctx.send(embed = emb4)
                else:
                    if count <0:
                        emb4 = discord.Embed(title=" Что-то пошло не так ",  description= f'\n▹ Значение должно быть равно 0 ', color=0xff9900)
                        emb4.set_footer(text=f'Отправлено: {ctx.author}  | Тест бот (c) 2022 •   ', icon_url=ctx.author.avatar_url,  )
                        message = await ctx.send(embed = emb4)
                    if count >5:
                            embed7 = discord.Embed(title="Что-то пошло не так", description=f"▹ Вы указали неверный уровень. Это должно быть число от 0 до 5", color=0xffff00)
                            await ctx.reply(embed=embed7)

                    else:
                        if _admin == 5:
                            if count == 0:
                                cursor.execute(f"update rayabot.users set admin = 0 where user_id = '{user.id}' and guild = '{ctx.guild.id}'")
                                connect.commit()
                                embed=discord.Embed(title=f'Вам cняли права администратора  на сервере `{ctx.guild.name}`', description=f'Команду выполнил: {ctx.message.author.mention}', color= 0xffff00)
                                await user.send(embed=embed)
                                    
                                embed1=discord.Embed(title= 'Выдача админ-прав' , description=f'Пользователь {user.mention} становиться обычным пользователем ', color=0xffff00)
                                embed1.add_field(name='Команду выполнил:', value=f'{ctx.message.author.mention}', inline=True)
                                await ctx.send(embed=embed1)

                            if count == 1:
                                cursor.execute(f"update rayabot.users set admin = 1 where user_id = '{user.id}' and guild = '{ctx.guild.id}'")
                                connect.commit()
                                embed=discord.Embed(title=f'Вам выдали `{count}` уровень администратора  на сервері `{ctx.guild.name}`', description=f'Команду выполнил: {ctx.message.author.mention}', color= 0xffff00)
                                await user.send(embed=embed)
                                
                                embed1=discord.Embed(title= 'Выдача админ-прав' , description=f'Пользователь {user.mention} получил {count} уровень администратора ', color=0xffff00)
                                embed1.add_field(name='Команду выполнил:', value=f'{ctx.message.author.mention}', inline=True)
                                await ctx.send(embed=embed1)

                            if count == 2:
                                cursor.execute(f"update rayabot.users set admin = 2 where user_id = '{user.id}' and guild = '{ctx.guild.id}'")
                                connect.commit()
                                embed=discord.Embed(title=f'Вам выдали `{count}` уровень администратора  на сервері `{ctx.guild.name}`', description=f'Команду выполнил: {ctx.message.author.mention}', color= 0xffff00)
                                await user.send(embed=embed)
                                    
                                embed1=discord.Embed(title= 'Выдача админ-прав' , description=f'Пользователь {user.mention} получил {count} уровень администратора ', color=0xffff00)
                                embed1.add_field(name='Команду выполнил:', value=f'{ctx.message.author.mention}', inline=True)
                                await ctx.send(embed=embed1) 

                            if count == 3:
                                cursor.execute(f"update rayabot.users set admin = 3 where user_id = '{user.id}' and guild = '{ctx.guild.id}'")
                                connect.commit()
                                embed=discord.Embed(title=f'Вам выдали `{count}` уровень администратора  на сервері `{ctx.guild.name}`', description=f'Команду выполнил: {ctx.message.author.mention}', color= 0xffff00)
                                await user.send(embed=embed)
                                    
                                embed1=discord.Embed(title= 'Выдача админ-прав' , description=f'Пользователь {user.mention} получил {count} уровень администратора ', color=0xffff00)
                                embed1.add_field(name='Команду выполнил:', value=f'{ctx.message.author.mention}', inline=True)
                                await ctx.send(embed=embed1)

                            if count == 4:
                                cursor.execute(f"update rayabot.users set admin = 4 where user_id = '{user.id}' and guild = '{ctx.guild.id}'")
                                connect.commit()
                                embed=discord.Embed(title=f'Вам выдали `{count}` уровень администратора  на сервері `{ctx.guild.name}`', description=f'Команду выполнил: {ctx.message.author.mention}', color= 0xffff00)
                                await user.send(embed=embed)
                                    
                                embed1=discord.Embed(title= 'Выдача админ-прав' , description=f'Пользователь {user.mention} получил {count} уровень администратора ', color=0xffff00)
                                embed1.add_field(name='Команду выполнил:', value=f'{ctx.message.author.mention}', inline=True)
                                await ctx.send(embed=embed1)

                            if count >=5:
                                embed7 = discord.Embed(title="Что-то пошло не так", description=f"▹ Максимальный уровень который вы можете выдать это - 4", color=0xffff00)
                                await ctx.reply(embed=embed7)

                        if _admin == 6:
                            if count == 0:
                                cursor.execute(f"update rayabot.users set admin = 0 where user_id = '{user.id}' and guild = '{ctx.guild.id}'")
                                connect.commit()
                                embed=discord.Embed(title=f'Вам cняли права администратора  на сервере `{ctx.guild.name}`', description=f'Команду выполнил: {ctx.message.author.mention}', color= 0xffff00)
                                await user.send(embed=embed)
                                    
                                embed1=discord.Embed(title= 'Выдача админ-прав' , description=f'Пользователь {user.mention} становиться обычным пользователем ', color=0xffff00)
                                embed1.add_field(name='Команду выполнил:', value=f'{ctx.message.author.mention}', inline=True)
                                await ctx.send(embed=embed1)

                            if count == 1:
                                cursor.execute(f"update rayabot.users set admin = 1 where user_id = '{user.id}' and guild = '{ctx.guild.id}'")
                                connect.commit()
                                embed=discord.Embed(title=f'Вам выдали `{count}` уровень администратора  на сервері `{ctx.guild.name}`', description=f'Команду выполнил: {ctx.message.author.mention}', color= 0xffff00)
                                await user.send(embed=embed)
                                
                                embed1=discord.Embed(title= 'Выдача админ-прав' , description=f'Пользователь {user.mention} получил {count} уровень администратора ', color=0xffff00)
                                embed1.add_field(name='Команду выполнил:', value=f'{ctx.message.author.mention}', inline=True)
                                await ctx.send(embed=embed1)

                            if count == 2:
                                cursor.execute(f"update rayabot.users set admin = 2 where user_id = '{user.id}' and guild = '{ctx.guild.id}'")
                                connect.commit()
                                embed=discord.Embed(title=f'Вам выдали `{count}` уровень администратора  на сервері `{ctx.guild.name}`', description=f'Команду выполнил: {ctx.message.author.mention}', color= 0xffff00)
                                await user.send(embed=embed)
                                    
                                embed1=discord.Embed(title= 'Выдача админ-прав' , description=f'Пользователь {user.mention} получил {count} уровень администратора ', color=0xffff00)
                                embed1.add_field(name='Команду выполнил:', value=f'{ctx.message.author.mention}', inline=True)
                                await ctx.send(embed=embed1) 

                            if count == 3:
                                cursor.execute(f"update rayabot.users set admin = 3 where user_id = '{user.id}' and guild = '{ctx.guild.id}'")
                                connect.commit()
                                embed=discord.Embed(title=f'Вам выдали `{count}` уровень администратора  на сервері `{ctx.guild.name}`', description=f'Команду выполнил: {ctx.message.author.mention}', color= 0xffff00)
                                await user.send(embed=embed)
                                    
                                embed1=discord.Embed(title= 'Выдача админ-прав' , description=f'Пользователь {user.mention} получил {count} уровень администратора ', color=0xffff00)
                                embed1.add_field(name='Команду выполнил:', value=f'{ctx.message.author.mention}', inline=True)
                                await ctx.send(embed=embed1) 

                            if count == 4:
                                cursor.execute(f"update rayabot.users set admin = 4 where user_id = '{user.id}' and guild = '{ctx.guild.id}'")
                                connect.commit()
                                embed=discord.Embed(title=f'Вам выдали `{count}` уровень администратора  на сервері `{ctx.guild.name}`', description=f'Команду выполнил: {ctx.message.author.mention}', color= 0xffff00)
                                await user.send(embed=embed)
                                    
                                embed1=discord.Embed(title= 'Выдача админ-прав' , description=f'Пользователь {user.mention} получил {count} уровень администратора ', color=0xffff00)
                                embed1.add_field(name='Команду выполнил:', value=f'{ctx.message.author.mention}', inline=True)
                                await ctx.send(embed=embed1)

                            if count == 5:
                                cursor.execute(f"update rayabot.users set admin = 5 where user_id = '{user.id}' and guild = '{ctx.guild.id}'")
                                connect.commit()
                                embed=discord.Embed(title=f'Вам выдали `{count}` уровень администратора  на сервері `{ctx.guild.name}`', description=f'Команду выполнил: {ctx.message.author.mention}', color= 0xffff00)
                                await user.send(embed=embed)
                                    
                                embed1=discord.Embed(title= 'Выдача админ-прав' , description=f'Пользователь {user.mention} получил {count} уровень администратора ', color=0xffff00)
                                embed1.add_field(name='Команду выполнил:', value=f'{ctx.message.author.mention}', inline=True)
                                await ctx.send(embed=embed1)
                             
                        


    except Exception as ex:
        print(ex)
            
@setadm.error
async def setadm_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        emb4 = discord.Embed(title=" Что-то пошло не так ",  description= f'\n▹ Упс, кажеться пользователь не найден. ', color=0xff9900)
        emb4.set_footer(text=f'Отправлено: {ctx.author}  | Тест бот (c) 2022 •   ', icon_url=ctx.author.avatar_url,  )
        message = await ctx.send(embed = emb4)



@bot.command(name = "popit", aliases = ["зщзше", "попіт"])
async def _popit(ctx):
        await ctx.reply("||:red_square:||||:red_square:||||:red_square:||||:red_square:||||:red_square:||||:red_square:||\n||:orange_square:||||:orange_square:||||:orange_square:||||:orange_square:||||:orange_square:||||:orange_square:||\n||:yellow_square:||||:yellow_square:||||:yellow_square:||||:yellow_square:||||:yellow_square:||||:yellow_square:||\n||:green_square:||||:green_square:||||:green_square:||||:green_square:||||:green_square:||||:green_square:||\n||:blue_square:||||:blue_square:||||:blue_square:||||:blue_square:||||:blue_square:||||:blue_square:||\n||:purple_square:||||:purple_square:||||:purple_square:||||:purple_square:||||:purple_square:||||:purple_square:||")




@bot.command()
async def image(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.author
        
    prapor = Image.open('prapor.jpg') #назва картинки в котру вставити аватар
    avatar = user.avatar_url_as(size = 128) #розмір аватара
    avt = BytesIO(await avatar.read())
    img = Image.open(avt)
    img = img.resize((280, 280))
    prapor.paste(img, (380, 80))#вставити аватар на картинку
    width, height = prapor.size
    draw = ImageDraw.Draw(prapor)
    text = "Слава Україні!"
    font = ImageFont.truetype('arial.ttf', 60) #розмір шрифта і назва
    textwidth, textheight = draw.textsize(text, font)
    x = 320
    y = 10 
    draw.text((x, y), text, font = font)#координати текста на фото
    prapor.save('image.jpg')#назва, під якою буде збережено у папці
    await ctx.send(file = discord.File("image.jpg"))


#--------------------------------------------------подключение бота---------------------------------------------------------------------------------------

try:
    bot.run(settings['token']) # Обращаемся к словарю settings с ключом token, для получения токена
except Exception as ex:
    print(ex)





