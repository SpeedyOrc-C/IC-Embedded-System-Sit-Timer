# The Website

The website is build on [SvelteKit](https://kit.svelte.dev/),
written in [TypeScript](https://www.typescriptlang.org/),
holding data in [PostgreSQL](https://www.postgresql.org/).

The pages are all in the folder [./src/routes](./src/routes),
where [(ad)](./src/routes/(ad)) holds the pages for advertising,
and [dashboard](./src/routes/dashboard) is for the users to see their logs.

This software works well without our website and hardware,
since they can make their own website and hardware and just call [our API](./src/routes/api) to log the data.
You can also hold the data in your own database, by providing the `DATABASE_URL` variable in your `.env` file.

## APIs

| API                              |  Verb  | Description                                                    |
|:---------------------------------|:------:|:---------------------------------------------------------------|
| `hello`                          |  GET   | Always returns "win" , indicate that the connection succeeded  |
| `sign-up`                        |  POST  | Sign up a new user                                             |
| `log-in`                         |  POST  | Log in a user and returns a session key                        |
| `log-out`                        |  POST  | Log out the from the current device                            |
| `log-out/all-places`             |  POST  | Log out the from all the devices                               |
| `device/pairing`                 |  POST  | Get a dynamic 4-digit hex code for pairing and a new device id |
| `device/pairing/<code>`          |  GET   | Pair the device with the code and add it to the user's account |
| `device/<id>`                    |  GET   | Tell whether this device exists                                |
| `device/<id>`                    | DELETE | Remove this device from the user's account                     |
| `device/<id>/name`               |  GET   | Get the name of the device                                     |
| `device/<id>/name`               |  PUT   | Set the name of the device                                     |
| `device/<id>/log/yes`            |  POST  | Log "sit" for this device with the current time                |
| `device/<id>/log/yes/<time-sec>` |  POST  | Log "sit" for this device with specified time in seconds       |
| `device/<id>/log/no`             |  POST  | Log "stand" for this device with the current time              |
| `device/<id>/log/no/<time-sec>`  |  POST  | Log "stand" for this device with specified time in seconds     |
