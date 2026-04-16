# Project B

We don't know the project yet, but to prepare ourselves as best as possible you can already do the setup below


## Setup

### clone this repo
``` 
git clone https://github.com/FeeElders-Protinus/project-b.git 
```
or with SSH
``` 
git clone git@github.com:FeeElders-Protinus/project-b.git 
```


### Lovable setup

make lovable account
[https://lovable.dev/](https://lovable.dev/)

After initial build with lovable, we will work **locally** using this repo

#### installs for local development
- install `Node.js` here [https://nodejs.org/en/download](https://nodejs.org/en/download)  
be sure to install the `windows installer .msi` file and not the `docker` env as this is not necessary
- inside this repo do `npm install`, which will all dependencies `lovable` needs for build/deploy

#### running locally
for simple local development and hosting start up a development server
```
npm run dev
```


to access the server from other devices run
```
npm run dev -- --host
```

#### Supabase as database
I didn't check this part, but apparently when using a Supabase we need to do this.  
- create a .env file at the root of the project with these contents which we'll find under  `project settings -> API`
```
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
```
