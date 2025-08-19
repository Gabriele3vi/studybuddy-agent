create table notes (
  id integer AUTO_INCREMENT PRIMARY key,
  name varchar(55),
  ext varchar(10),
  upload_timestamp datetime not null default CURRENT_TIMESTAMP
); 

create table note_chunks (
  id integer AUTO_INCREMENT PRIMARY key,
  note_id varchar(55),
  chunck_order integer,
  content text,
  embedding VECTOR(1536),
  VECTOR INDEX idx_embedding ((VEC_COSINE_DISTANCE(embedding)))
)