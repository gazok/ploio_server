# CONVENTIONS

## Commit Messages

```plaintext
type: summary

body

footer
```

|     Type | Desc                                              |
|---------:|:--------------------------------------------------|
|      add | add files                                         |
|     feat | add feature                                       |
|      fix | fix bugs                                          |
|     docs | update documents                                  |
|    style | code formatting without changing the flow of code |
| refactor | refactoring                                       |
|     test | add testing code                                  |
|    chore | change that do not relate to a fix or feature     |

### Body

```
- src/multiline.py:
    - Detailed change 1
    - Detailed change 2
- src/hello.py: Detailed change 3
...
```

Subscribes which file has changed, why file had to be changed, what is changed on file.

### Footer

```
type: #issue-number
```

Subscribe issue tracker id.

|       Type | Desc                              |
|-----------:|:----------------------------------|
|      Fixes | am fixing issue (not yet fixed)   |
|   Resolves | resolved issue                    |
|        Ref | refer to specific issue           |
| Related to | refer to specific not fixed issue |

