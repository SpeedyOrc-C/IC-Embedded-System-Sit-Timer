import {DB} from "$lib/DB"

export async function POST({request})
{
    try
    {
        const {username, password} = await request.json()

        try
        {
            await DB.SignUp(username, password)
        }
        catch (e)
        {
            return new Response("User already exists", {status: 409})
        }
    }
    catch (e)
    {
        return new Response("Missing Parameters [username] [password]", {status: 400})
    }

    return new Response("Win")
}
