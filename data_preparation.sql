CREATE INDEX idx_audio_features_id ON audio_features (id);
CREATE INDEX idx_tracks_id ON tracks (id);
CREATE INDEX idx_r_track_artist_track_id ON r_track_artist (track_id);
CREATE INDEX idx_r_track_artist_artist_id ON r_track_artist (artist_id);
CREATE INDEX idx_artists_id ON artists (id);

CREATE TEMP TABLE track_info AS
WITH track_info_with AS (
	SELECT
		af.id,
		tr.name,
		GROUP_CONCAT(rta.artist_id, ', ') AS artist_id,
		GROUP_CONCAT(ar.name, ', ') AS artist_name
	FROM audio_features af
	LEFT JOIN tracks tr ON af.id = tr.id
	LEFT JOIN r_track_artist rta ON af.id = rta.track_id
	LEFT JOIN artists ar ON rta.artist_id = ar.id
	GROUP BY af.id
)
SELECT * FROM track_info_with;

CREATE INDEX  idx_track_info_ids ON track_info (id);

SELECT
    af.id,
    ti.name,
    ti.artist_id,
    ti.artist_name,
    af.acousticness,
    af.danceability,
    af.energy,
    af.instrumentalness,
    af.key,
    af.liveness,
    af.loudness,
    af.mode,
    af.speechiness,
    af.tempo,
    af.time_signature,
    af.valence
FROM audio_features af
INNER JOIN track_info ti ON af.id = ti.id;