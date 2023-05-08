## Frontend setup
In this cloned version of the app everything should be set up and ready to go.

For the frontend to work the backend should be running too.
The backend address is set in the frontend/src/lib/client/core/OpenApi.ts file.

If you want to set up the frontend from scratch, you can follow the instructions below.

To install the needed packages, run:
```bash
npm run install
```

To compile SCSS to static css, you need to have smui-theme installed (with ```npm run install```):
```bash
npm run prepare
```

Generating client code:
```bash
# for this to work the backend should be running on 127.0.0.1:8000
npm run generate-client
```
After the client code is generated, you have to set the desired backend address in the generated file
frontend/src/lib/client/core/OpenApi.ts. The address should be set in the OpenApiConfig object at the end of the file:
```typescript
export const OpenAPI: OpenAPIConfig = {
    BASE: ' http://127.0.0.1:8000',
    VERSION: '0.1.0-alpha',
    WITH_CREDENTIALS: false,
    CREDENTIALS: 'include',
    TOKEN: undefined,
    USERNAME: undefined,
    PASSWORD: undefined,
    HEADERS: undefined,
    ENCODE_PATH: undefined,
};
```

## Developing
```bash
# after the dependencies are installed you can run the server locally
npm run dev
```

## Building
To create a production version of the SentimentAnalysisApp:
```bash
npm run build
```

To preview the production build run: `npm run preview`.

## Deploying
To deploy the build/index.js using Node, run:
```bash
node build/index.js
# if the port 3000 is already in use, you can specify a different port
# PORT=3001 node build/index.js
```
For this to work, you need to have the dependencies installed and svelte.config.js configured to use 'adapter-node'.
This can be done by removing the comments from the line 2 in svelte.config.js of this project.
Also the corresponding dependency needs to be installed:
```bash
npm -i @sveltejs/adapter-node
```


