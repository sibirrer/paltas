import numpy as np
import pandas as pd
import unittest
import sys, glob, copy, os
from paltas import generate

# Define the cosmos path
cosmos_folder = 'test_data/cosmos/'


class GenerateTests(unittest.TestCase):

	def setUp(self):
		# Set the random seed so we don't run into trouble
		np.random.seed(20)

	def test_parse_args(self):
		# Check that the argument parser works as intended
		# We have to modify the sys.argv input which is bad practice
		# outside of a test
		old_sys = copy.deepcopy(sys.argv)
		sys.argv = ['test','config_dict.py','save_folder',
			'--n','1000']
		args = generate.parse_args()
		self.assertEqual(args.config_dict,'config_dict.py')
		self.assertEqual(args.save_folder,'save_folder')
		self.assertEqual(args.n,1000)
		sys.argv = old_sys

	def test_main(self):
		# Test that the main function makes some images
		old_sys = copy.deepcopy(sys.argv)
		output_folder = 'test_data/test_dataset'
		sys.argv = ['test','test_data/config_dict.py',output_folder,'--n','10']
		generate.main()

		image_file_list = glob.glob(os.path.join(output_folder,'image_*.npy'))

		self.assertEqual(len(image_file_list),10)

		# Make sure all of the files are readable and have the correct size
		# for the config
		for image_file in image_file_list:
			img = np.load(image_file)
			self.assertTupleEqual(img.shape,(64,64))
			os.remove(image_file)

		# Make sure the metadata makes sense
		metadata = pd.read_csv(os.path.join(output_folder,'metadata.csv'))
		self.assertEqual(len(metadata),10)
		self.assertListEqual(list(
			metadata['cosmology_parameters_cosmology_name']),['planck18']*10)
		self.assertListEqual(list(
			metadata['detector_parameters_pixel_scale']),[0.08]*10)
		self.assertListEqual(list(metadata['subhalo_parameters_c_0']),
			[18.0]*10)
		self.assertListEqual(list(metadata['main_deflector_parameters_z_lens']),
			[0.5]*10)
		self.assertListEqual(list(metadata['source_parameters_z_source']),
			[1.5]*10)
		self.assertGreater(np.std(metadata['source_parameters_catalog_i']),0)
		self.assertListEqual(list(metadata['psf_parameters_fwhm']),
			[0.1]*10)
		# Check that the subhalo_parameters_sigma_sub are being drawn
		self.assertGreater(np.std(metadata['los_parameters_delta_los']),
			0.0)
		# Check that nothing is getting written under cross_object
		for key in metadata.keys():
			self.assertFalse('cross_object' in key)
			self.assertFalse('source_exclusion_list' in key)

		# Remove the metadata file
		os.remove(os.path.join(output_folder,'metadata.csv'))
		os.remove(os.path.join(output_folder,'config_dict.py'))

		sys.argv = old_sys

		# Also clean up the test cosmos cache
		test_cosmo_folder = 'test_data/cosmos/'
		os.remove(test_cosmo_folder+'paltas_catalog.npy')
		for i in range(10):
			os.remove(test_cosmo_folder+'npy_files/img_%d.npy'%(i))
		os.rmdir(test_cosmo_folder+'npy_files')

	def test_main_drizzle(self):
		# Test that the main function makes some images
		old_sys = copy.deepcopy(sys.argv)
		output_folder = 'test_data/test_dataset'
		sys.argv = ['test','test_data/config_dict_drizz.py',output_folder,
			'--n','10']
		generate.main()

		image_file_list = glob.glob(os.path.join(output_folder,'image_*.npy'))

		self.assertEqual(len(image_file_list),10)

		# Make sure all of the files are readable and have the correct size
		# for the config
		for image_file in image_file_list:
			img = np.load(image_file)
			self.assertTupleEqual(img.shape,(85,85))
			os.remove(image_file)

		# Make sure the metadata makes sense
		metadata = pd.read_csv(os.path.join(output_folder,'metadata.csv'))
		self.assertEqual(len(metadata),10)
		self.assertListEqual(list(
			metadata['cosmology_parameters_cosmology_name']),['planck18']*10)
		self.assertListEqual(list(
			metadata['detector_parameters_pixel_scale']),[0.08]*10)
		self.assertListEqual(list(metadata['subhalo_parameters_c_0']),
			[18.0]*10)
		self.assertListEqual(list(metadata['main_deflector_parameters_z_lens']),
			[0.5]*10)
		self.assertListEqual(list(metadata['source_parameters_z_source']),
			[1.5]*10)
		self.assertGreater(np.std(metadata['source_parameters_catalog_i']),0)
		self.assertListEqual(list(metadata['psf_parameters_fwhm']),
			[0.1]*10)
		# Check that the subhalo_parameters_sigma_sub are being drawn
		self.assertGreater(np.std(metadata['los_parameters_delta_los']),
			0.0)
		# Check that nothing is getting written under cross_object
		for key in metadata.keys():
			self.assertFalse('cross_object' in key)
			self.assertFalse('source_exclusion_list' in key)

		# Remove the metadata file
		os.remove(os.path.join(output_folder,'metadata.csv'))
		os.remove(os.path.join(output_folder,'config_dict_drizz.py'))

		sys.argv = old_sys

		# Also clean up the test cosmos cache
		test_cosmo_folder = 'test_data/cosmos/'
		os.remove(test_cosmo_folder+'paltas_catalog.npy')
		for i in range(10):
			os.remove(test_cosmo_folder+'npy_files/img_%d.npy'%(i))
		os.rmdir(test_cosmo_folder+'npy_files')
