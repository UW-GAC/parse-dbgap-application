version 1.0

workflow parse_dbgap_application {
    input {
        File application_pdf
    }
    call extract_dars {
        input: application_pdf = application_pdf
    }
    output {
        File dar_file = extract_dars.dar_file
    }
    meta {
        author: "Adrienne Stilp"
        email: "amstilp@uw.edu"
    }
}


task extract_dars {
    input {
        File application_pdf
    }

    command <<<
        python /usr/local/parse_dbgap_application/parse_dars.py \
            ~{application_pdf} \
            ~{dar_file}
    >>>

    output {
        File dar_file = "dar_file.tsv"
    }

    runtime {
        docker: "uwgac/parse_dbgap_application:0.0.1"
    }
}
