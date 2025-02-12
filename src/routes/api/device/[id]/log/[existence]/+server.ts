import {DB} from "$lib/DB";

export async function POST({params: {id, existence}})
{
    let win: boolean

    switch (existence)
    {
        case "yes":
            win = await DB.Log(id, true)
            break
        case "no":
            win = await DB.Log(id, false)
            break
        default:
            return new Response("Parameter existence must be \"yes\" or \"no\"", {status: 400})
    }

    if (!win)
    {
        return new Response("Device not found or duplicated record", {status: 400})
    }

    return new Response("WIN")
}
