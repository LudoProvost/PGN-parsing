import zstandard as zstd

def decompress_zst(file_path, output_path):
    with open(file_path, 'rb') as compressed:
        with open(output_path, 'wb') as decompressed:
            dctx = zstd.ZstdDecompressor()
            dctx.copy_stream(compressed, decompressed)

# Example usage
input_zst_file = 'compressed_db/lichess_db_standard_rated_2014-09.pgn.zst'
output_pgn_file = 'decompressed_db/lichess_db_standard_rated_2014-09.pgn'
decompress_zst(input_zst_file, output_pgn_file)