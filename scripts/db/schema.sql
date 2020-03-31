/**
 * Copyright ©2020. The Regents of the University of California (Regents). All Rights Reserved.
 *
 * Permission to use, copy, modify, and distribute this software and its documentation
 * for educational, research, and not-for-profit purposes, without fee and without a
 * signed licensing agreement, is hereby granted, provided that the above copyright
 * notice, this paragraph and the following two paragraphs appear in all copies,
 * modifications, and distributions.
 *
 * Contact The Office of Technology Licensing, UC Berkeley, 2150 Shattuck Avenue,
 * Suite 510, Berkeley, CA 94720-1620, (510) 643-7201, otl@berkeley.edu,
 * http://ipira.berkeley.edu/industry-info for commercial licensing opportunities.
 *
 * IN NO EVENT SHALL REGENTS BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
 * INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF
 * THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF REGENTS HAS BEEN ADVISED
 * OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 * REGENTS SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE
 * SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED HEREUNDER IS PROVIDED
 * "AS IS". REGENTS HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES,
 * ENHANCEMENTS, OR MODIFICATIONS.
 */

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;
SET search_path = public, pg_catalog;
SET default_tablespace = '';
SET default_with_oids = false;


--

CREATE TYPE approver_types AS ENUM (
    'admin',
    'instructor'
);

--

CREATE TYPE email_template_types AS ENUM (
    'admin_alert_instructor_change',
    'admin_alert_room_change',
    'invitation',
    'notify_instructor_of_changes',
    'recordings_scheduled',
    'room_change_no_longer_eligible',
    'waiting_for_approval'
);

--

CREATE TYPE publish_types AS ENUM (
    'canvas',
    'kaltura_media_gallery'
);

--

CREATE TYPE recording_types AS ENUM (
    'presentation_audio',
    'presenter_audio',
    'presenter_presentation_audio'
);

--

CREATE TYPE room_capability_types AS ENUM (
    'screencast',
    'screencast_and_video'
);

--

CREATE TABLE admin_users (
    id integer NOT NULL,
    uid character varying(255) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);
ALTER TABLE admin_users OWNER TO diablo;
CREATE SEQUENCE admin_users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE admin_users_id_seq OWNER TO diablo;
ALTER SEQUENCE admin_users_id_seq OWNED BY admin_users.id;
ALTER TABLE ONLY admin_users ALTER COLUMN id SET DEFAULT nextval('admin_users_id_seq'::regclass);
ALTER TABLE ONLY admin_users
    ADD CONSTRAINT admin_users_pkey PRIMARY KEY (id);
ALTER TABLE ONLY admin_users
    ADD CONSTRAINT admin_users_uid_key UNIQUE (uid);

--

CREATE TABLE approvals (
    approved_by_uid VARCHAR(80) NOT NULL,
    section_id INTEGER NOT NULL,
    term_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    approver_type approver_types,
    publish_type publish_types NOT NULL,
    recording_type recording_types NOT NULL,
    created_at timestamp with time zone NOT NULL
);
ALTER TABLE approvals OWNER TO diablo;
ALTER TABLE approvals ADD CONSTRAINT approvals_pkey PRIMARY KEY (approved_by_uid, section_id, term_id);
CREATE INDEX approvals_approved_by_uid_idx ON approvals USING btree (approved_by_uid);
CREATE INDEX approvals_section_id_idx ON approvals USING btree (section_id);
CREATE INDEX approvals_term_id_idx ON approvals USING btree (term_id);

--

CREATE TABLE canvas_course_sites (
    canvas_course_site_id INTEGER NOT NULL,
    section_id INTEGER NOT NULL,
    term_id INTEGER NOT NULL,
    canvas_course_site_name TEXT NOT NULL,
    created_at timestamp with time zone NOT NULL
);
ALTER TABLE canvas_course_sites OWNER TO diablo;
ALTER TABLE canvas_course_sites ADD CONSTRAINT canvas_course_sites_pkey PRIMARY KEY (canvas_course_site_id, section_id, term_id);
CREATE INDEX canvas_course_sites_canvas_course_site_id_idx ON canvas_course_sites USING btree (canvas_course_site_id);
CREATE INDEX canvas_course_sites_section_id_idx ON canvas_course_sites USING btree (section_id);
CREATE INDEX canvas_course_sites_term_id_idx ON canvas_course_sites USING btree (term_id);

--

CREATE TABLE email_templates (
    id INTEGER NOT NULL,
    template_type email_template_types NOT NULL,
    name VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    subject_line VARCHAR(255) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);
ALTER TABLE email_templates OWNER TO diablo;
CREATE SEQUENCE email_templates_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE email_templates_id_seq OWNER TO diablo;
ALTER SEQUENCE email_templates_id_seq OWNED BY email_templates.id;
ALTER TABLE ONLY email_templates ALTER COLUMN id SET DEFAULT nextval('email_templates_id_seq'::regclass);
ALTER TABLE ONLY email_templates
    ADD CONSTRAINT email_templates_pkey PRIMARY KEY (id);
ALTER TABLE ONLY email_templates
    ADD CONSTRAINT email_templates_name_unique_constraint UNIQUE (name);

--

CREATE TABLE emails_sent (
    id INTEGER NOT NULL,
    recipient_uids VARCHAR(80)[] NOT NULL,
    section_id INTEGER NOT NULL,
    template_type email_template_types NOT NULL,
    term_id INTEGER NOT NULL,
    sent_at timestamp with time zone NOT NULL
);
ALTER TABLE emails_sent OWNER TO diablo;
CREATE SEQUENCE emails_sent_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE emails_sent_id_seq OWNER TO diablo;
ALTER SEQUENCE emails_sent_id_seq OWNED BY emails_sent.id;
ALTER TABLE ONLY emails_sent ALTER COLUMN id SET DEFAULT nextval('emails_sent_id_seq'::regclass);
ALTER TABLE ONLY emails_sent
    ADD CONSTRAINT emails_sent_pkey PRIMARY KEY (id);
CREATE INDEX emails_sent_section_id_idx ON emails_sent USING btree (section_id);

--

CREATE TABLE rooms (
    id INTEGER NOT NULL,
    capability room_capability_types,
    is_auditorium BOOLEAN NOT NULL,
    kaltura_resource_id INTEGER,
    location VARCHAR(255) NOT NULL,
    created_at timestamp with time zone NOT NULL
);
ALTER TABLE rooms OWNER TO diablo;
CREATE SEQUENCE rooms_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE rooms_id_seq OWNER TO diablo;
ALTER SEQUENCE rooms_id_seq OWNED BY rooms.id;
ALTER TABLE ONLY rooms ALTER COLUMN id SET DEFAULT nextval('rooms_id_seq'::regclass);
ALTER TABLE ONLY rooms
    ADD CONSTRAINT rooms_pkey PRIMARY KEY (id);
ALTER TABLE ONLY rooms
    ADD CONSTRAINT rooms_location_unique_constraint UNIQUE (location);
CREATE INDEX rooms_location_idx ON rooms USING btree (location);

--

CREATE TABLE scheduled (
    section_id INTEGER NOT NULL,
    term_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    created_at timestamp with time zone NOT NULL
);
ALTER TABLE scheduled OWNER TO diablo;
ALTER TABLE scheduled ADD CONSTRAINT scheduled_pkey PRIMARY KEY (section_id, term_id);
CREATE INDEX scheduled_section_id_idx ON scheduled USING btree (section_id);
CREATE INDEX scheduled_term_id_idx ON scheduled USING btree (term_id);

--

ALTER TABLE ONLY approvals
    ADD CONSTRAINT approvals_room_id_fkey FOREIGN KEY (room_id) REFERENCES rooms(id);
ALTER TABLE ONLY scheduled
    ADD CONSTRAINT scheduled_room_id_fkey FOREIGN KEY (room_id) REFERENCES rooms(id);

--
