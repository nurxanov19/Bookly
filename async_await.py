import asyncio

async def first(sec):
    print('first function is going...')
    await asyncio.sleep(sec)
    print('frist function end')


async def second(sec):
    print('second function is going...')
    await asyncio.sleep(sec)
    print('second function end')

async def third(sec):
    print('third function is going...')
    await asyncio.sleep(sec)
    print('third function end')

async def main():
    print('main function is going ...')
    result1, result2, result3 = await asyncio.gather(first(2), second(3), third(1))


if __name__ == '__main__':
    asyncio.run(main())
    print('main function end')

