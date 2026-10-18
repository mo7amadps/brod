import discord

def is_owner(member: discord.Member) -> bool:
    return bool(member.guild and member.guild.owner_id == member.id)
