# pip install librosa essentia madmom soundfile sqlalchemy
import librosa, numpy as np, json, soundfile as sf
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, MetaData, Boolean
import madmom

engine = create_engine("sqlite:///djagent.db")
md = MetaData()
tracks = Table("tracks", md,
    Column("id", Integer, primary_key=True),
    Column("path", String, unique=True),
    Column("bpm", Float), Column("key", String), Column("key_conf", Float),
    Column("loudness", Float), Column("energy", Float),
    Column("duration", Float),
    Column("phrase_grid", String), Column("sections", String),
    Column("stems_cached", Boolean, default=False),
)
md.create_all(engine)

def analyze_track(path):
    y, sr = librosa.load(path, mono=True)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, trim=True, units='time')
    downbeat_proc = madmom.features.downbeats.RNNDownBeatProcessor()
    db_act = downbeat_proc(path)
    db_tracker = madmom.features.downbeats.DBNDownBeatTrackingProcessor(beats_per_bar=[4], fps=100)
    downbeats = db_tracker(db_act)  # [time, beat_in_bar]
    phrase_starts = [float(t) for t,b in downbeats if b == 1.0][::8]  # every 8 bars as phrase
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr).mean(axis=1)
    key_index = int(np.argmax(chroma))
    key_names = ['C','C#','D','Eb','E','F','F#','G','Ab','A','Bb','B']
    key = key_names[key_index]
    S = np.abs(librosa.stft(y))
    rms = librosa.feature.rms(S=S).mean()
    energy = float(np.clip(rms*10, 0, 1))
    duration = librosa.get_duration(y=y, sr=sr)
    # simple structural segmentation
    boundaries = librosa.segment.agglomerative(np.cov(S), k=6)
    secs = [float(librosa.frames_to_time(int(b))) for b in np.unique(boundaries)]
    with engine.begin() as cn:
        cn.execute(tracks.insert().values(
            path=path, bpm=float(tempo), key=key, key_conf=1.0,
            loudness=float(librosa.power_to_db(S**2).mean()),
            energy=energy, duration=duration,
            phrase_grid=json.dumps(phrase_starts),
            sections=json.dumps(secs),
            stems_cached=False
        ))

# analyze_track("/path/to/track.wav")
