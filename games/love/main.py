import random

async def calculate_love(ctx, name_one, name_two):
    percent = random.randint(0, 100)
    await ctx.send("There is " + str(percent) + "% love between " + name_one.display_name + " and " + name_two.display_name + "!")
