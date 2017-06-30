```
user@52.206.170.132:shorten> \d url
+-------------+-----------------------------+---------------------------------------------------+
| Column      | Type                        | Modifiers                                         |
|-------------+-----------------------------+---------------------------------------------------|
| id          | bigint                      |  not null default nextval('url_id_seq'::regclass) |
| created_on  | timestamp without time zone |                                                   |
| modified_on | timestamp without time zone |                                                   |
| url         | character varying           |                                                   |
+-------------+-----------------------------+---------------------------------------------------+
Indexes:
    "url_pkey" PRIMARY KEY, btree (id)
    "url_url_key" UNIQUE CONSTRAINT, btree (url)

Time: 1.713s (a second)
user@52.206.170.132:shorten>
```