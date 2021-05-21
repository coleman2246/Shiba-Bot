#!/usr/bin/python3
import BotInit
import asyncio

threads = []
bot_instances = [BotInit.ShibHolderUpdates(),BotInit.ShibPriceUpdates(),
                BotInit.GasPriceUpdate(), BotInit.ShibHolderUpdates(),
                BotInit.LeashPriceUpdates(), BotInit.LeashHolderUpdates(),
                BotInit.HourVolumeUpdate(), BotInit.ShibMarketCapUpdates(),
                BotInit.ShibInformer()]

loop = asyncio.get_event_loop()

for i in bot_instances:
    loop.create_task(i.bot.start(i.key))


loop.run_forever()
