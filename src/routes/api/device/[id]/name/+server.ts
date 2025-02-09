import {DB} from "$lib/DB";

export async function GET({cookies, params: {id}})
{
    const key = cookies.get("session-key")

    if (key === undefined)
    {
        return new Response("Unauthorized", {status: 401})
    }

    const name = await DB.GetDeviceName(key, id)

    if (name === null)
    {
        return new Response("Unauthorized or device not found", {status: 404})
    }

    return new Response(name)
}

export async function PUT({cookies, request, params: {id}})
{
    const key = cookies.get("session-key")

    if (key === undefined)
    {
        return new Response("Unauthorized", {status: 401})
    }

    const newName = await request.text()

    const win = await DB.SetDeviceName(key, id, newName)

    if (!win)
    {
        return new Response("Unauthorized or device not found", {status: 404})
    }

    return new Response("WIN")
}
