# How to Create CTF Challenges for PicoCTF

## At a glance

**Step 1:** Read what makes a **good** CTF by reading [The Many Maxims of
Maximally Effective CTFs](http://54.212.176.14/maxims.html).

**Step 2:** Install the required software for challenge development. All challenges are
containerized, deployed with `cmgr`, and stored on Github.

**Step 3:** Create challenges.

**Step 4:** Play test your challenges with `cmgr update` and `cmgr playtest`.

## Install required software

- Install docker from (https://docs.docker.com/engine/install/).
- Install [cmgr](https://github.com/picoCTF/cmgr). You can either build from
  scratch or install a pre-compiled version. Make sure you put it somewhere
  in your path, e.g., `/usr/local/bin/cmgr`.
- Install `git` as you will need to commit all challenges.
- Clone this GitHub repo to your namespace, say as `picoctf-challenges`.
- Checkout with `git checkout <challenge repo>`
- Look at example problems and trouble shooting guides at
  https://github.com/picoCTF/start-problem-dev and https://github.com/picoCTF/cmgr

At this point, you should have `picoctf-challenges` on your local file system.
You now need to configure `cmgr` so it knows where challenges are, and where
to store artifacts.

```bash
mkdir cmgr cmgr/artifacts
export CMGR_DB=`pwd`/cmgr/cmgr.db
export CMGR_ARTIFACTS_DIR=`pwd`/cmgr/artifacts
```

**Recommended:** Set the above variables as part of login by adding to your
`.bashrc` or `.zshrc`

```bash
echo "export CMGR_DB =`pwd`/cmgr.db" >> ~/.bashrc
echo "export CMGR_ARTIFACTS_DIR=`pwd`/artifacts" >> ~/.bashrc
source .bashrc
```

## Creating Challenges

A challenge consists of four parts:

1.  The challenge code you write.
2.  `problem.md` that describes the challenge, points, and how to connect to
    the running challenge.
3.  `Dockerfile` with **additional** special `cmgr` directives and code.
4.  `solve/` directory with a solve script.

Your life will be much easier if you understand `cmgr` before writing a
challenge. It can be a little tricky to deal with.

### Understanding cmgr

`cmgr` serves up containerized challenges, and creates new challenge instances
based on your challenge definition to handle load and perform cheat detection.
To do so, it handles:

- Challenge instances creation from a template.
- Translating a `problem.md` describing the challenge into something the UI
  can show.
- Building the challenge from the template, creating the flag, and creating
  any artifacts the player needs to solve the challenge.
- Dynamically assigning a port to an instance
- Cheat detection

When you write a challenge, you are creating a
template for how `cmgr` should run the challenge. An actual running challenge
we call an **instance**. Each instance is a unique container with its own
flag and port. It's important to keep the distinction in mind.

- The `problem.md` gives a _Description_ that is shown to the user when they
  navigate to a challenge, and _Details_ for a running instance such as the
  assigned port number.
- `cmgr update` adds the challenge to the database, build 1 or more images
  from the `Dockerfile`.
- `cmgr playtest` runs an image locally with a playtest interface.

**Port Concept** As we will see, your `Dockerfile` will have a `# PUBLISH AS <name>`
statement that is case-sensitive. The actual port assigned by `cmgr` is
substituted into `name` in the problem **Details** section of the UI.

### Understanding why cmgr, cheat detection, and scaling challenges

**Cheat Detection:** Traditionally CTFs have a single flag shared by all
players. Unfortunately, people cheat. A lot. We estimate up to 40% of picoctf
players share flags with each other, which is cheating. It's like signing up
for a marathon, only to have someone drive you to the end.

One way to guard against cheating is to create a fresh challenge variation --
called a **challenge instance** per
player or team. `cmgr` takes a challenge and creates new instances
automatically.

The simplest challenge instance just varies the flag. For example, we may have two
instances where instance 1 has the flag `flag_instance1` and instance 2
has the flag `flag_instance2`.

- When a player starts a challenge, they are assigned an instance.
- If the player submits a valid flag for their instance, they get points.
- If the player submits a valid flag for _someone elses instance_, you know
  they are cheating.

`cmgr` implements this idea at build time. The `cmgr` administrator decides
how many instances to create, and they are round-robin assigned to users as
they play the contest.

**Scaling** Contests like picoctf also need to scale as we may have tens of thousands of
users playing a single challenge. To do so, `cmgr` again uses the idea of an
instance. Players are dynamically assigned an instance at play-time.

**Intuition**: With the above, the main problems `cmgr` solves are:

- Specifying a CTF challenge.
- Creating multiple instances of a challenge at build time. Each instance is
  its own container image.
- Making sure each instance has its own port and flag, and registering it with
  the picoctf server.

### The `problem.md` file

The basic definition of a challenge is given in the `problem.md` file, which
specify how a challenge instance in a container are registered with the
server. The `problem.md` file has:

- Challenge name as the H1 title.
- A static description used for all instances.
- A dynamic details that is specific per instance, e.g., the port the
  challenge was assigned to.
- Hints
- Metadata such as which CTF event that challenge is for, points,
  namespacing, the category, etc.

Here is a sample challenge `problem.md`

```markdown
# My Awesome Challenge

- Namespace: picoctf # Challenge names are unique within a namespace.
- Type: custom # Typical default
- Category: binary # crypto, web, etc.
- Points: 1 # Update with real points

## Description

This portion of the challenge description is displayed to users regardless of whether an instance of the challenge is currently running.

You can also include `{{url_for("file", "display text")}}` as a link to an artifact needed to solve the challenge, e.g., the binary, source code, etc.

## Details

This portion of the challenge description is displayed to users when an instance of a challenge is
running. It may include any content permitted in the "Description" section, as well as the following
instance-specific templates:

- `{{http_base("port_name")}}`: URL prefix for HTTP requests to `PUBLISH AS port_name` in the `Dockerfile.
- `{{server("port_name")}}`: hostname which hosts for connecting to the
  associated port for the challenge
- `{{port("port_name")}}`: The specific port for the running instance.
- `{{link("port_name", "/url/in/challenge")}}`: convenience wrapper for generating an HTML link)
- `{{link_as("port_name", "/url/in/challenge", "display text")}}`: convenience
  wrapper for generating an HTML link with text different from the URL

## Hints

- A list of hints for the end user.
- The hints are all templatable.
- Whether there is a cost for displaying them is up to the front-end system

## Tags

- optional tag1
- optional tag2

## Attributes

- Organization: ACI
- event: 18739-ctf # The name of the CTF event
```

**Note:** The `port_name` must tie to a `PUBLISH AS` statement in the
`Dockerfile.

### Challenge Containers

Every challenge is a container specified by a `Dockerfile` with _one
additional field_ called the `PUBLISH` statement.

**Flag Location:** `cmgr` looks for the flag location in
`/challenge/metadata.json`.

There are two approaches:

- Small groups: make it a static flag. This means you
  don't get cheat detection.
- Normal: use `ARG FLAG`, and use
  [setup-challenge.py](https://github.com/picoCTF/start-problem-dev/blob/master/example-problems/reversing-python/setup-challenge.py)

**Port Assignments:**
A typical `Dockerfile` contains a hard-coded `EXPOSE` directive for ports:

```yaml
EXPOSE 5555
```

`cmgr` requires that you add a `Dockerfile` comment that assigns a variable
name to the port being published for all network challenges. The variable
name is given with `PUBLISH` as a comment. We use comments to not interfere
with normal `Dockerfile` parsing.

```yaml
# Same as before, with the PUBLISH  <port> AS <name> as a comment that has
# semantic meaning in cmgr.
EXPOSE 5555
# PUBLISH 5555 AS myvar
```

When `cmgr` builds a problem, it:

- Assigns a port to the challenge.
- Routes the assigned port to the `EXPOSE` port
- Substitutes in the assigned port for the port variable name in each
  instance per the `problem.md` file.

As a result, ports are never the static number from `EXPOSE` -- they are
assigned by `cmgr`.

```markdown
You can connect to the CTF challenge with:
`ssh -p {{port("myvar")}} ctf-player@{{server("myvar")}}` using password
`{{lookup("password")}}`
```

There is nothing special about the word `myvar` -- you could call it `foobaz`.
It's just a variable.

_Warning:_ The `PUBLISH` line is the most annoying and easy-to-get wrong in
challenge development. Worse, `cmgr` swallows docker build errors, so often
you don't know why it's failing.

- `cmgr` is case-sensitive: you must have the keywords `PUBLISH` and `AS` in
  uppercase.
- This must be in a comment _after_ the `EXPOSE` directive.
- When in doubt, cut-and-paste the above using your own variable name.

## Building Challenges

Once you specify the `Dockerfile`, create the code, and write `problem.md`,
you are ready to play test. We cannot emphasize enough how important play
testing is.

```bash
cmgr update # quick
cmgr playtest # slow -- it does the actual build

# Play test web interface will be running at http://localhost:4242/
```

## Next Steps

- Look at example problems.
- Set debugging by enabling logging, e.g., `CMGR_LOGGING=info cmgr playtest <challenge>`
- Create, play test, iterate.
