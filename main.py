import os
import time
import threading
import asyncio
import uvicorn

from fastapi import FastAPI, Query

app = FastAPI(title="Unique UID generator API")

POW_2_40 = 2**40
POW_2_12 = 2**12
POW_2_8 = 2**8
POW_2_4 = 2**4

COUNTER_LOCK: asyncio.Lock = asyncio.Lock()
COUNTER_TRACKER: dict[str, int] = {}


async def uid_generator() -> str:
    current_mstime_mod_2_40 = int(time.time() * 1000) % POW_2_40
    process_id_mod_2_4 = os.getpid() % POW_2_4
    thread_id_mod_2_8 = threading.get_native_id() % POW_2_8    

    counter_check_string = (
        str(current_mstime_mod_2_40) + "$" +
        str(process_id_mod_2_4) + "$" +
        str(thread_id_mod_2_8) + "$"
    )

    async with COUNTER_LOCK:
        if counter_check_string in COUNTER_TRACKER:
            COUNTER_TRACKER[counter_check_string] += 1
        else:
            COUNTER_TRACKER.clear()
            COUNTER_TRACKER[counter_check_string] = 1
        
        counter_mod_2_12 = COUNTER_TRACKER[counter_check_string] % POW_2_12

    uid = current_mstime_mod_2_40 << 24
    uid |= process_id_mod_2_4 << 20
    uid |= thread_id_mod_2_8 << 12
    uid |= counter_mod_2_12

    return str(uid)


@app.get(
    "/get-uid-batch",
    description="Get unique UID in batches",
    response_model=list[str]
)
async def get_uid_batch(
    batch_size: int = Query(1, ge=1, le=4000, alias='batch-size', description="Batch size")
) -> list[str]:
    return await asyncio.gather(*[uid_generator() for _ in range(batch_size)])


if __name__ == "__main__":
    uvicorn.run("main:app", use_colors=False, reload=True)
