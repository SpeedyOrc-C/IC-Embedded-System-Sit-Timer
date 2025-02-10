import {DB} from "$lib/DB";

export async function GET({params: {id}})
{
    const win = await DB.DoesDeviceExist(id)

    if (!win)
    {
        return new Response("Device not found", {status: 404})
    }

    return new Response("Hi!")
}

export async function DELETE({cookies, params: {id}})
{
    const key = cookies.get("session-key")

    if (key === undefined)
    {
        return new Response("Unauthorized", {status: 401})
    }

    const win = await DB.DeleteDevice(key, id)

    if (!win)
    {
        return new Response("Unauthorized or device not found", {status: 404})
    }

    return new Response("WIN")
}
