#!/bin/sh

if [ -f /tmp/memos_prod.db ]; then
  echo "Copying database..."
  mv /tmp/memos_prod.db /var/opt/memos/memos_prod.db
  content="Congratulations! Your flag is \`$(cat /flag)\`"
  sqlite3 /var/opt/memos/memos_prod.db "update memo set content='$content' where id=2;"
fi

/usr/local/memos/memos
