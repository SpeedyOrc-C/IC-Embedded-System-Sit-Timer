import {DB, type LogResponse} from "$lib/DB";

export async function POST({params: {id, existence}})
{
    let result: LogResponse

    switch (existence)
    {
        case "yes":
            result = await DB.Log(id, true)
            break
        case "no":
            result = await DB.Log(id, false)
            break
        default:
            return new Response("Parameter existence must be \"yes\" or \"no\"", {status: 400})
    }

    switch (result)
    {
        case "inserted":
            return new Response("WIN")
        case "duplicated":
            return new Response("Duplicated record", {status: 202})
        case "invalid-device":
            return new Response("Device not found", {status: 404})
    }
}
