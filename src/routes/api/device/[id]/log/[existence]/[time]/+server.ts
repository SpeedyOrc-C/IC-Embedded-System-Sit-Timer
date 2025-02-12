import {DB} from "$lib/DB";

export async function POST({params: {id, existence, time}})
{
    const timeInt = parseInt(time)

    if (isNaN(timeInt))
    {
        return new Response("Invalid timestamp", {status: 400})
    }

    let win: boolean

    switch (existence)
    {
        case "yes":
            win = await DB.Log(id, true, timeInt)
            break
        case "no":
            win = await DB.Log(id, false, timeInt)
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
