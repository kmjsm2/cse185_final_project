% Define the file path for the FPKM file
fpkm_file_path = '/Users/zoekim/Desktop/cse_final/GSE268233_FPKM.csv';

% Step 1: Read the FPKM file
fpkm_data = readtable(fpkm_file_path, 'FileType', 'text', 'Delimiter', ',', 'ReadVariableNames', true);

% Display the first few rows of the FPKM data to understand its structure
disp('FPKM data:');
disp(head(fpkm_data));

% Extract sample names (assuming samples are from the second column onwards)
sample_names = fpkm_data.Properties.VariableNames(2:end);

% Convert FPKM data to matrix for easy manipulation
fpkm_matrix = table2array(fpkm_data(:, 2:end));

% Gene IDs (assuming they are in the first column)
gene_ids = fpkm_data.(1);

% Define the output directory
output_dir = '/Users/zoekim/Desktop/cse_final/fpkm_val';

% Create and save separate tables for each sample
for i = 1:length(sample_names)
    sample_name = sample_names{i};
    fpkm_data_export = table(gene_ids, fpkm_matrix(:, i), 'VariableNames', {'gene_id', 'FPKM'});
    output_file = fullfile(output_dir, [sample_name, '_fpkm.csv']);
    % writetable(fpkm_data_export, output_file);
    disp(['FPKM file saved to ', output_file]);
end
