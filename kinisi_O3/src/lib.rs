#[pyo3::pymodule]
mod kinisi_O3 {
    use pyo3::prelude::*;

    #[pyfunction]
    fn compute_convariance_matrix(
        size: usize,
        n_samples: Vec<f64>,
        data_variances: Vec<f64>,
    ) -> PyResult<Vec<Vec<f64>>> {
        let mut cov = vec![vec![0.0; size]; size];

        for i in 0..size {
            for j in i..size {
                let ratio: f64 = n_samples[i] / n_samples[j];
                let value: f64 = ratio * data_variances[i];
                
                cov[i][j] = value;
                cov[j][i] = value;
            }
        }
            
        Ok(cov)
    }
}
