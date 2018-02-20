###IMPALA: **I**dentifying **M**ovie **P**lot events by **A**na<b>L</b>ysing sentiment and **A**udio

##**Project Structure:**

#**data:** All files that are used as data-input like subtitles, movie scripts, audio etc
**audio_csvfiles:** Raw audio energy of single movies partitioned into 1 second intervals
**audiosent_csvfiles:** Csv files for sentiment scores and audio energy of scenes. Audio is partitioned into three or sometimes four classes/levels (silent, medium, loud, loudest)
**audiosent_csv_raw:** Csv files for sentiment scores and audio energy of scenes. This time with raw audio values instead of classes
**genre_csvfiles:** Experimental csvfiles for movie script genre classification. Each of the around 900 movie scripts has one or multiple genres associated to it
**manually_annotated:** Movie scripts with manually annotated time codes

#**results:** 

**correlation_txtfiles:** Temporary text files containing information about correlation, p-value for various movies, sentiment methods and correlation coefficients (spearman, pearson, kendall's tau)
**graphs:** Various graphs plotted using matplotlib

#**src:** Source code

**src_audio:** Audio analysis

**src_ml:** Currently experimental scripts/modules for machine learning
**src_text:** Modules for text preprocessing and analysis
lexicons: Sentiment lexicons
preprocessing: Parsing of srt subtitles and fountain movie scripts into xml files, automatic time code annotation of movie scripts, extraction of information from the xml files
sentiment: utilities for getting sentiment scores for subtitles and movie scripts
