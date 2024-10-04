CREATE SEQUENCE IF NOT EXISTS trip_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE IF NOT EXISTS "public"."trip" (
    "id" integer DEFAULT nextval('trip_id_seq') NOT NULL,
    "start_date" timestamp NOT NULL,
    "end_date" timestamp NOT NULL,
    "currency" character(3) NOT NULL,
    "outbound_cost" numeric(20,2) NOT NULL,
    "outbound_airport" character(3) NOT NULL,
    "outbound_airline" character varying(255) NOT NULL,
    "outbound_fly_number" character varying(16) NOT NULL,
    "return_cost" numeric(20,2) NOT NULL,
    "return_airport" character(3) NOT NULL,
    "return_airline" character varying(255) NOT NULL,
    "return_fly_number" character varying(16) NOT NULL,
    CONSTRAINT "trip_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

CREATE INDEX IF NOT EXISTS "trip_end_date" ON "public"."trip" USING btree ("end_date");
CREATE INDEX IF NOT EXISTS "trip_start_date" ON "public"."trip" USING btree ("start_date");
CREATE INDEX IF NOT EXISTS "trip_outbound_airport" ON "trip" ("outbound_airport");

ALTER TABLE "public"."trip" ADD COLUMN IF NOT EXISTS "duration_nights" smallint DEFAULT NULL;
ALTER TABLE "public"."trip" ADD COLUMN IF NOT EXISTS "meals_amount" smallint DEFAULT NULL;
ALTER TABLE "public"."trip" ADD COLUMN IF NOT EXISTS "rent_cost" numeric(20,2) DEFAULT NULL;
ALTER TABLE "public"."trip" ADD COLUMN IF NOT EXISTS "meal_cost" numeric(20,2) DEFAULT NULL;