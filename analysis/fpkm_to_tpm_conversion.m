% FPKM file directory
fpkm_file_path = '/Users/zoekim/Desktop/cse_final/GSE268233_FPKM.csv';

% Read the FPKM file
fpkm_data = readtable(fpkm_file_path, 'FileType', 'text', 'Delimiter', ',', 'ReadVariableNames', true);

% Extract sample names (assuming samples are from the second column onwards)
sample_names = fpkm_data.Properties.VariableNames(2:end); 

% Get value FPKM in matrix 
fpkm_matrix = table2array(fpkm_data(:, 2:end)); 

% Create and save separate tables for each FPKM sample
gene_ids = fpkm_data.(1);
output_dir_fpkm = '/Users/zoekim/Desktop/cse_final/fpkm_val';
for i = 1:length(sample_names)
    sample_name = sample_names{i};
    fpkm_data_export = table(gene_ids, fpkm_matrix(:, i), 'VariableNames', {'gene_id', 'FPKM'});
    output_file_fpkm = fullfile(output_dir_fpkm, [sample_name, '_fpkm.csv']);
    % writetable(fpkm_data_export, output_file_fpkm);
end

% Convert FPKM to TPM
sum_fpkm = sum(fpkm_matrix, 1); % Calculate the sum of FPKM for each sample
tpm_matrix = (fpkm_matrix ./ sum_fpkm) * 1e6; % Convert FPKM to TPM

% Create and save separate tables for each TPM sample
output_dir_tpm = '/Users/zoekim/Desktop/cse_final/tpm_val';
for i = 1:length(sample_names)
    sample_name = sample_names{i};
    tpm_data_export = table(gene_ids, tpm_matrix(:, i), 'VariableNames', {'gene_id', 'TPM'});
    output_file_tpm = fullfile(output_dir_tpm, [sample_name, '_tpm.csv']);
    % writetable(tpm_data_export, output_file_tpm);
end
