# Gossamer

Markup for those who hate to look at HTML

## Prolouge

An honest attempt at making an HTML alternative. This project stems from the fact that while I believe web development is amazing, HTML has never been a language
that I have enjoyed to look at. There are also so many oddities about the language, such as hyperlinks using the <em>a</em> (anchor) tag. There doesn't seem to be anything intuitive
about this naming convension. There are many, many other instances where HTML seems to have made questionable decisions. I also wanted this new 'language' I am creating to
actually be readable, instead of being a wall of shrunken down words such as <em>div</em>, <em>ol</em>, <em>li</em>, etc.

## Features

### Gossamer Layout File

Instead of using the claustrophobic tag styles of HTML, I decided to used a more spaced out and clearer tag.

To start, all tags now use camel case in their names instead of all lower case. Instead of using an opening and closing tag, 
you simply declare the name of the tag, then put an opening and closing bracket in, and put all child tags inside of these
brackers (it's supposed to look C or Java-like).

```
TagName {
  /* child tags go here */
}
```

Just like HTML tags, Gossamer tags can accept ids and classes. Ids and classes are listed between the tag name
and the opening bracket. An id is prepended with <em>#</em> and a class is prepended with <em>.</em> similar to CSS.
Tags can have multiple classes, but only at most one id.

```
TagName #id .class1 .class2 {
  /* child tags go here */
}
```

Tag attributes are written inside the braces FIRST, before any child tags are added. These attributes look similar to CSS.
All current attributes for all existing tags are compatible.
You simply need to put them in the Gossamer format. Here is an example of a tag with attributes:

```
Image {
  source: assets/images/image.png
  description: An image
  
  /* child tags go here */
}
```

Some common attributes have been renamed in order to be clearer. Here is a complete list:

```
src -> source
href -> destination
alt -> description
```

Many tags also have either bad names, or shortened names that have been replaced. Here is a complete list:

```
div -> Container
p -> Text
img -> Image
a -> Link (will deal with html's actual link tag soon)
ol -> OrderedList
ul -> UnorderedList
li -> ListItem
nav -> Navigation
```

### Gossamer Styles File

The style sheet for Gossamer is nearly identical to SCSS, with a few extra additions to make life easier.
For example, I added a new position called <em>center</em> which centers an objects inside a container with relative
positioning.

Gossamer has build in media queries that make life easier. For example, you can use the following instead of size media
queries:

```
Container {
  /* desktop styles */
  font-size: 128px
  
  /* tablet styles */
  self.tablet {
    font-size: 64px
  }
  
  /* phone styles */
  self.phone {
    font-size: 32px
  }
}
```

Notice the use of the <em>self</em> keyword. This refers to the tag itSELF. So the styles in this case for each device size
apply to the Container tag.

The self keyword is also used in replacement of &: that SCSS uses. For example:

```
SCSS:

div {
  background: blue
  
  &:hover {
    background: red
  }
}

Gossamer:

Container {
  background: blue
  
  self.hover {
    background: red
  }
}
```

## Creating a Project

The file <em>gossamer.sh</em> contains several commands that can be used to create, build, and configure gossamer 'projects'.

To create a new project, run the following command:
```
./gossamer.sh new project-name-here
```

To create a component, run the following command:
```
./gossamer.sh component project-name-here component-name-here
```

To build the project, run the following command:
```
./gossamer.sh build project-name-here
```

Once the project builds, a 'build' folder will be created in the project folder that contains the generated HTML and CSS

## Examples

This repository has two examples of Gossamer code. The demo folder contains a simple demo that demonstrates the majority
of Gossamer's functionality. The gossamer-web folder contains the code for the github page for Gossamer, which I decided
to write in Gossamer since it would be pointless to create a markup language and not use it.

## Issues

This project is a WORK IN PROGRESS. The interpreter I wrote has no error checking implemented, so try Gossamer at your own risk!
If the interpreter runs into an infinite loop, I am sorry :(. I also am still figuring out what else I can do with Gossamer, so there may be more features ahead.

The python code I have allows you to create Gossamer 'projects', but I will be making a version that converts single files since
I feel this would be more useful. I am considering seeing how well Gossamer plays with Angular, so stay tuned!
