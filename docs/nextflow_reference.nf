// Authored-but-not-executed reference: the real Nextflow pipeline
// this project would run in production (QC -> alignment -> variant
// calling, containerized per stage). No Nextflow runtime is
// available in this environment, so src/pipeline_stages.py
// implements the identical QC/call stage sequence in Python as the
// executed mirror, and all measured results in this repo come from
// that mirror.
nextflow.enable.dsl = 2

process QC_FILTER {
    container 'biocontainers/samtools:1.19'
    input: tuple val(sample_id), path(bam)
    output: tuple val(sample_id), path("${sample_id}.filtered.bam")
    script: "samtools view -b -q 20 ${bam} > ${sample_id}.filtered.bam"
}

process CALL_VARIANTS {
    container 'broadinstitute/gatk:4.5.0.0'
    input: tuple val(sample_id), path(bam)
    output: tuple val(sample_id), path("${sample_id}.vcf")
    script: "gatk HaplotypeCaller -I ${bam} -O ${sample_id}.vcf"
}

workflow {
    samples_ch = Channel.fromFilePairs("data/*.bam")
    filtered_ch = QC_FILTER(samples_ch)
    CALL_VARIANTS(filtered_ch)
}
