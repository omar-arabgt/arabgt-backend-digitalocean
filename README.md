## Overview

Arabgt Project


## Installation

```docker-compose up --build ```

## Import existing data on mysql

```docker exec -i arabgt_mysql mysql -uroot -prootpassword qbtbherhgs < /path/data.sql```


## Import existing users from csv

```docker exec -it arabgt_web /bin/bash```
```python import_user.py```
