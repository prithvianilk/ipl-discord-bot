import discord 

def get_help():
    commands = [
            '`$score` - Gives live score of ongoing IPL match',
            '`$table` - Gives entire points table of the IPL season',
            '`$orange-cap` - Gives the current Orange Cap holder of the IPL season',
            '`$purple-cap` - Gives the current Purple Cap holder of the IPL season',
        ]
    embedVar_help = discord.Embed(title = "Commands", color = 0xFFD700)
    embedVar_help.add_field(name = "List of Commands\n", value = '\n\n'.join(commands), inline=False)
    return embedVar_help