BATCH YOUTUBE AUDIO SNIPPETS

1) Install dependencies:
   - yt-dlp
   - ffmpeg

2) Edit snippets.csv with your own rows:
   Columns: url,start,end,output,format
   - start/end can be SS(.ms) or HH:MM:SS(.ms)

3) Run:
   python batch_audio_snippets.py --csv snippets.csv --format m4a --outdir snippets --tempdir downloads

4) Options:
   --precise  -> re-encode for exact cuts (slower, high quality)
   --format   -> default output format for rows missing the 'format' column

Outputs will be in ./snippets (or your chosen --outdir).