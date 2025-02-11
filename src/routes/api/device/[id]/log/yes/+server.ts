import {DB} from "$lib/DB";

export async function POST({params: {id}})
{
    const win = await DB.LogYes(id)

    if (!win)
    {
        return new Response("Device not found", {status: 404})
    }

    return new Response("WIN")
}
